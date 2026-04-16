from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers
from .models import Cliente, Carro
import re
import json


# ── Utilitários ───────────────────────────────────────────────────────────────

def email_valido(email):
    return re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email)


def render_erro(request, clientes_list, erro, campos={}):
    """Retorna o template de clientes com a mensagem de erro e campos preenchidos."""
    return render(request, 'clientes.html', {
        'clientes': clientes_list,
        'erro': erro,
        **campos
    })


# ── Views ─────────────────────────────────────────────────────────────────────

def clientes(request):
    clientes_list = Cliente.objects.all()

    if request.method == 'GET':
        return render(request, 'clientes.html', {'clientes': clientes_list})

    if request.method != 'POST':
        return HttpResponse(status=405)

    # Dados pessoais
    nome      = request.POST.get('nome', '').strip()
    sobrenome = request.POST.get('sobrenome', '').strip()
    email     = request.POST.get('email', '').strip()
    cpf       = request.POST.get('cpf', '').strip()
    telefone  = request.POST.get('telefone', '').strip()

    # Endereço
    cep    = request.POST.get('cep', '').strip()
    rua    = request.POST.get('rua', '').strip()
    numero = request.POST.get('numero', '').strip()
    bairro = request.POST.get('bairro', '').strip()
    cidade = request.POST.get('cidade', '').strip()
    estado = request.POST.get('estado', '').strip()

    # Carros
    carros = request.POST.getlist('carro')
    placas = request.POST.getlist('placa')
    anos   = request.POST.getlist('ano')
    tipos  = request.POST.getlist('tipo')
    cores  = request.POST.getlist('cor')

    # Campos para repopular o formulário em caso de erro
    campos = {
        'nome': nome, 'sobrenome': sobrenome, 'email': email,
        'cpf': cpf, 'telefone': telefone,
        'cep': cep, 'rua': rua, 'numero': numero,
        'bairro': bairro, 'cidade': cidade, 'estado': estado,
    }

    # ── Validações de campos obrigatórios ──
    if not nome or not sobrenome:
        return render_erro(request, clientes_list, 'Nome e sobrenome são obrigatórios.', campos)

    if not cpf:
        return render_erro(request, clientes_list, 'CPF é obrigatório.', campos)

    if not email:
        return render_erro(request, clientes_list, 'E-mail é obrigatório.', campos)

    # ── Validação de formato de e-mail ──
    if not email_valido(email):
        return render_erro(request, clientes_list, 'E-mail inválido.', campos)

    # ── Validações de duplicidade ──
    if Cliente.objects.filter(cpf=cpf).exists():
        return render_erro(request, clientes_list, 'Este CPF já está cadastrado.', campos)

    if telefone and Cliente.objects.filter(telefone=telefone).exists():
        return render_erro(request, clientes_list, 'Este telefone já está cadastrado.', campos)

    if email and Cliente.objects.filter(email=email).exists():
        return render_erro(request, clientes_list, 'Este e-mail já está cadastrado.', campos)

    for placa in placas:
        if placa and Carro.objects.filter(placa=placa).exists():
            return render_erro(request, clientes_list, f'A placa {placa} já está cadastrada.', campos)

    # ── Salvamento ──
    cliente = Cliente.objects.create(
        nome=nome, sobrenome=sobrenome, email=email,
        cpf=cpf, telefone=telefone,
        cep=cep, rua=rua, numero=numero,
        bairro=bairro, cidade=cidade, estado=estado,
    )

    for carro, placa, ano, tipo, cor in zip(carros, placas, anos, tipos, cores):
        if carro and placa:
            Carro.objects.create(
                carro=carro, placa=placa, ano=ano or None,
                tipo=tipo or None, cor=cor or None,
                cliente=cliente
            )

    return redirect(reverse('clientes'))


def att_cliente(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    id_cliente = request.POST.get('id_cliente')
    if not id_cliente:
        return HttpResponse(status=400)

    cliente = get_object_or_404(Cliente, id=id_cliente)
    carros  = Carro.objects.filter(cliente=cliente)

    cliente_json = json.loads(serializers.serialize('json', [cliente]))[0]
    carros_json  = json.loads(serializers.serialize('json', carros))
    carros_json  = [{'fields': c['fields'], 'id': c['pk']} for c in carros_json]

    data = {
        'cliente_id': cliente_json['pk'],
        'cliente':    cliente_json['fields'],
        'carros':     carros_json,
    }
    return JsonResponse(data)


def excluir_carro(request, id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    carro      = get_object_or_404(Carro, id=id)
    id_cliente = carro.cliente.id
    carro.delete()

    return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id_cliente}')


def update_carro(request, id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    nome_carro = request.POST.get('carro', '').strip()
    placa      = request.POST.get('placa', '').strip()
    ano        = request.POST.get('ano', '').strip()
    tipo       = request.POST.get('tipo', '').strip()
    cor        = request.POST.get('cor', '').strip()

    if not nome_carro or not placa:
        return HttpResponse('Modelo e placa são obrigatórios.', status=400)

    carro = get_object_or_404(Carro, id=id)

    if Carro.objects.exclude(id=id).filter(placa=placa).exists():
        return HttpResponse('Placa já existente', status=400)

    carro.carro = nome_carro
    carro.placa = placa
    carro.ano   = ano or None
    carro.tipo  = tipo or None
    carro.cor   = cor or None
    carro.save()

    return HttpResponse(id)


def update_cliente(request, id):
    if request.method != 'POST':
        return JsonResponse({'status': '405', 'erro': 'Método não permitido.'}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': '400', 'erro': 'JSON inválido.'}, status=400)

    cliente = get_object_or_404(Cliente, id=id)

    novo_email = body.get('email', '').strip()
    novo_cpf   = body.get('cpf', '').strip()
    novo_tel   = body.get('telefone', '').strip()

    # ── Validação de formato de e-mail ──
    if novo_email and not email_valido(novo_email):
        return JsonResponse({'status': '400', 'erro': 'E-mail inválido.'}, status=400)

    # ── Validações de duplicidade ──
    if novo_cpf and Cliente.objects.exclude(id=id).filter(cpf=novo_cpf).exists():
        return JsonResponse({'status': '400', 'erro': 'Este CPF já pertence a outro cliente.'}, status=400)

    if novo_tel and Cliente.objects.exclude(id=id).filter(telefone=novo_tel).exists():
        return JsonResponse({'status': '400', 'erro': 'Este telefone já pertence a outro cliente.'}, status=400)

    if novo_email and Cliente.objects.exclude(id=id).filter(email=novo_email).exists():
        return JsonResponse({'status': '400', 'erro': 'Este e-mail já pertence a outro cliente.'}, status=400)

    try:
        cliente.nome      = body.get('nome',      cliente.nome).strip()
        cliente.sobrenome = body.get('sobrenome',  cliente.sobrenome).strip()
        cliente.email     = novo_email   or cliente.email
        cliente.cpf       = novo_cpf     or cliente.cpf
        cliente.telefone  = novo_tel     or cliente.telefone
        cliente.cep       = body.get('cep',    cliente.cep)
        cliente.rua       = body.get('rua',    cliente.rua)
        cliente.numero    = body.get('numero', cliente.numero)
        cliente.bairro    = body.get('bairro', cliente.bairro)
        cliente.cidade    = body.get('cidade', cliente.cidade)
        cliente.estado    = body.get('estado', cliente.estado)

        cliente.save()
        return JsonResponse({'status': '200'}, status=200)

    except Exception as e:
        # Log interno — não expõe detalhes ao cliente
        print(f'[update_cliente] Erro inesperado: {e}')
        return JsonResponse({'status': '500', 'erro': 'Erro interno ao salvar.'}, status=500)