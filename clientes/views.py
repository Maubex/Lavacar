from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Cliente, Carro
import re
import json


def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})

    elif request.method == "POST":
        # Dados pessoais
        nome      = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email     = request.POST.get('email')
        cpf       = request.POST.get('cpf')
        telefone  = request.POST.get('telefone')

        # Endereço
        cep    = request.POST.get('cep')
        rua    = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        # Carros
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos   = request.POST.getlist('ano')

        # Verifica se CPF já existe
        if Cliente.objects.filter(cpf=cpf).exists():
            return render(request, 'clientes.html', {
                'nome': nome, 'sobrenome': sobrenome, 'email': email,
                'cpf': cpf, 'telefone': telefone,
                'cep': cep, 'rua': rua, 'numero': numero,
                'bairro': bairro, 'cidade': cidade, 'estado': estado,
                'carros': zip(carros, placas, anos),
                'erro': 'CPF já cadastrado.'
            })

        # Valida e-mail
        if not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
            return render(request, 'clientes.html', {
                'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf,
                'telefone': telefone,
                'cep': cep, 'rua': rua, 'numero': numero,
                'bairro': bairro, 'cidade': cidade, 'estado': estado,
                'carros': zip(carros, placas, anos),
                'erro': 'E-mail inválido.'
            })

        # Cria o cliente
        cliente = Cliente(
            nome      = nome,
            sobrenome = sobrenome,
            email     = email,
            cpf       = cpf,
            telefone  = telefone,
            cep       = cep,
            rua       = rua,
            numero    = numero,
            bairro    = bairro,
            cidade    = cidade,
            estado    = estado,
        )
        cliente.save()

        # Cria os carros vinculados
        for carro, placa, ano in zip(carros, placas, anos):
            if carro and placa:  # só salva se tiver modelo e placa preenchidos
                Carro(carro=carro, placa=placa, ano=ano, cliente=cliente).save()

        return redirect(reverse('clientes'))


def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente    = get_object_or_404(Cliente, id=id_cliente)
    carros     = Carro.objects.filter(cliente=cliente)

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
    carro = get_object_or_404(Carro, id=id)
    id_cliente = carro.cliente.id
    carro.delete()
    return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id_cliente}')


@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa      = request.POST.get('placa')
    ano        = request.POST.get('ano')

    carro = get_object_or_404(Carro, id=id)

    # Verifica se a placa já existe em outro carro
    if Carro.objects.exclude(id=id).filter(placa=placa).exists():
        return HttpResponse('Placa já existente')

    carro.carro = nome_carro
    carro.placa = placa
    carro.ano   = ano
    carro.save()

    return HttpResponse(id)


def update_cliente(request, id):
    body = json.loads(request.body)

    cliente = get_object_or_404(Cliente, id=id)
    try:
        # Dados pessoais
        cliente.nome      = body.get('nome',      cliente.nome)
        cliente.sobrenome = body.get('sobrenome',  cliente.sobrenome)
        cliente.email     = body.get('email',      cliente.email)
        cliente.cpf       = body.get('cpf',        cliente.cpf)
        cliente.telefone  = body.get('telefone',   cliente.telefone)

        # Endereço
        cliente.cep    = body.get('cep',    cliente.cep)
        cliente.rua    = body.get('rua',    cliente.rua)
        cliente.numero = body.get('numero', cliente.numero)
        cliente.bairro = body.get('bairro', cliente.bairro)
        cliente.cidade = body.get('cidade', cliente.cidade)
        cliente.estado = body.get('estado', cliente.estado)

        cliente.save()
        return JsonResponse({'status': '200'})
    except Exception as e:
        return JsonResponse({'status': '500', 'erro': str(e)})