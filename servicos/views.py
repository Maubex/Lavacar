from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from .models import TipoServico, CategoriaVeiculo, TabelaPreco, OrdemServico, Adicional
from clientes.models import Cliente, Carro


# ── Mapa tipo do carro → categoria de preço ──────
MAPA_CATEGORIA = {
    'hatch':       'Veículo Pequeno',
    'sedan':       'Veículo Médio',
    'suv':         'Veículo SUV Grande',
    'caminhonete': 'Veículo Grande',
    'pickup':      'Veículo Grande',
    'van':         'Veículo Grande',
    'moto':        'Veículo Pequeno',
    'esportivo':   'Veículo Médio',
    'outro':       'Veículo Médio',
}


def get_categoria_por_carro(carro):
    nome = MAPA_CATEGORIA.get(carro.tipo, 'Veículo Médio')
    return CategoriaVeiculo.objects.filter(nome=nome).first()


def tem_perfil(user, *perfis):
    """Verifica se o usuário tem um dos perfis informados."""
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=perfis).exists()


# ══════════════════════════════════════════════════
# DASHBOARD — apenas gerente e admin
# ══════════════════════════════════════════════════

@login_required(login_url='login')
def dashboard(request):
    # Funcionário não tem acesso ao dashboard
    if not tem_perfil(request.user, 'gerente', 'admin'):
        return redirect('servicos_home')

    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str    = request.GET.get('data_fim')

    if not data_inicio_str or not data_fim_str:
        data_fim    = timezone.now().date()
        data_inicio = data_fim - timedelta(days=30)
    else:
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim    = datetime.strptime(data_fim_str,    '%Y-%m-%d').date()
        except ValueError:
            data_fim    = timezone.now().date()
            data_inicio = data_fim - timedelta(days=30)

    qs = OrdemServico.objects.filter(data__date__range=[data_inicio, data_fim])

    total_lavagens    = qs.count()
    faturamento_total = qs.aggregate(Sum('preco'))['preco__sum'] or 0
    ticket_medio      = qs.aggregate(Avg('preco'))['preco__avg'] or 0

    servicos_mais_vendidos = qs.values('tipo_servico__nome').annotate(
        qtd=Count('tipo_servico__nome')
    ).order_by('-qtd')[:5]

    top_clientes = Cliente.objects.filter(
        carros__ordens__in=qs
    ).annotate(
        qtd_servicos=Count('carros__ordens')
    ).order_by('-qtd_servicos')[:5]

    hoje     = timezone.now().date()
    qs_hoje  = OrdemServico.objects.filter(data__date=hoje)
    os_hoje  = qs_hoje.count()
    fat_hoje = qs_hoje.aggregate(Sum('preco'))['preco__sum'] or 0

    return render(request, 'servicos/dashboard.html', {
        'total_lavagens':         total_lavagens,
        'faturamento_total':      faturamento_total,
        'ticket_medio':           ticket_medio,
        'servicos_mais_vendidos': servicos_mais_vendidos,
        'top_clientes':           top_clientes,
        'data_inicio':            data_inicio.strftime('%Y-%m-%d'),
        'data_fim':               data_fim.strftime('%Y-%m-%d'),
        'os_hoje':                os_hoje,
        'fat_hoje':               fat_hoje,
    })


# ══════════════════════════════════════════════════
# BUSCA — tela principal de atendimento
# ══════════════════════════════════════════════════

@login_required(login_url='login')
def servicos_home(request):
    return render(request, 'servicos/servicos.html')


@login_required(login_url='login')
def servicos_buscar(request):
    if request.method != 'POST':
        return JsonResponse({'status': '404'})

    query = request.POST.get('query', '').strip().upper()
    if not query:
        return JsonResponse({'status': '404'})

    carro = Carro.objects.filter(placa__iexact=query).first()
    if carro:
        return JsonResponse({'status': '200', 'tipo': 'placa', 'carro': _carro_json(carro)})

    cliente = None
    if query.isdigit():
        cliente = Cliente.objects.filter(id=query).first()
    if not cliente:
        cliente = Cliente.objects.filter(cpf__iexact=query).first()

    if cliente:
        carros = Carro.objects.filter(cliente=cliente)
        return JsonResponse({
            'status':  '200',
            'tipo':    'cliente',
            'cliente': {'id': cliente.pk, 'nome': cliente.nome, 'sobrenome': cliente.sobrenome},
            'carros':  [_carro_resumo(c) for c in carros],
        })

    return JsonResponse({'status': '404', 'query': query})


@login_required(login_url='login')
def servicos_carro_json(request, carro_pk):
    carro = get_object_or_404(Carro, pk=carro_pk)
    return JsonResponse({'status': '200', 'carro': _carro_json(carro)})


# ══════════════════════════════════════════════════
# CADASTRO RÁPIDO
# ══════════════════════════════════════════════════

@login_required(login_url='login')
def servicos_cadastrar_carro(request):
    placa    = request.GET.get('placa', '').upper()
    clientes = Cliente.objects.all().order_by('nome')

    if request.method == 'POST':
        modelo     = request.POST.get('modelo', '').strip()
        placa      = request.POST.get('placa', '').strip().upper()
        tipo       = request.POST.get('tipo', '')
        cor        = request.POST.get('cor', '')
        ano        = request.POST.get('ano', '')
        cliente_id = request.POST.get('cliente_id', '')

        if cliente_id:
            cliente = get_object_or_404(Cliente, pk=cliente_id)
        else:
            cliente, _ = Cliente.objects.get_or_create(
                nome='Anônimo',
                defaults={'sobrenome': ''}
            )

        if Carro.objects.filter(placa=placa).exists():
            return render(request, 'servicos/cadastrar_carro.html', {
                'erro':     'Placa já cadastrada.',
                'placa':    placa,
                'clientes': clientes,
            })

        Carro.objects.create(
            carro=modelo, placa=placa, tipo=tipo,
            cor=cor, ano=ano if ano else None, cliente=cliente,
        )

        return redirect(reverse('servicos_home') + f'?placa={placa}')

    return render(request, 'servicos/cadastrar_carro.html', {
        'placa':    placa,
        'clientes': clientes,
    })


# ══════════════════════════════════════════════════
# BUSCAR PREÇO
# ══════════════════════════════════════════════════

@login_required(login_url='login')
def buscar_preco(request):
    carro_id   = request.GET.get('carro_id')
    servico_id = request.GET.get('servico_id')

    try:
        carro     = Carro.objects.get(pk=carro_id)
        servico   = TipoServico.objects.get(pk=servico_id)
        categoria = get_categoria_por_carro(carro)

        if not categoria:
            return JsonResponse({'status': '404', 'erro': 'Categoria não encontrada'})

        tabela = TabelaPreco.objects.get(
            tipo_servico=servico,
            categoria_veiculo=categoria
        )
        return JsonResponse({'status': '200', 'preco': str(tabela.preco)})

    except (Carro.DoesNotExist, TipoServico.DoesNotExist, TabelaPreco.DoesNotExist):
        return JsonResponse({'status': '404', 'erro': 'Preço não encontrado'})


# ══════════════════════════════════════════════════
# NOVA ORDEM DE SERVIÇO
# ══════════════════════════════════════════════════

@login_required(login_url='login')
def nova_ordem(request, carro_pk):
    carro      = get_object_or_404(Carro, pk=carro_pk)
    categoria  = get_categoria_por_carro(carro)
    adicionais = Adicional.objects.filter(ativo=True)

    servicos_com_preco = []
    for s in TipoServico.objects.filter(ativo=True):
        preco = None
        if categoria:
            try:
                tabela = TabelaPreco.objects.get(
                    tipo_servico=s,
                    categoria_veiculo=categoria
                )
                preco = tabela.preco
            except TabelaPreco.DoesNotExist:
                preco = None
        s.preco = preco
        servicos_com_preco.append(s)

    if request.method == 'POST':
        servico_id     = request.POST.get('servico_id')
        adicionais_ids = request.POST.getlist('adicionais')
        observacao     = request.POST.get('observacao', '')
        preco_total    = request.POST.get('preco', 0)

        servico = get_object_or_404(TipoServico, pk=servico_id)

        ordem = OrdemServico.objects.create(
            carro=carro, tipo_servico=servico,
            preco=preco_total, observacao=observacao,
            status='aguardando',
        )

        if adicionais_ids:
            adicionais_objs = Adicional.objects.filter(pk__in=adicionais_ids)
            ordem.adicionais.set(adicionais_objs)

        return redirect(reverse('servicos_home') + f'?placa={carro.placa}')

    return render(request, 'servicos/form_ordem.html', {
        'carro':      carro,
        'servicos':   servicos_com_preco,
        'adicionais': adicionais,
        'categoria':  categoria,
    })


# ══════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════

def _carro_json(carro):
    historico = []
    for os in carro.ordens.select_related('tipo_servico').all():
        historico.append({
            'tipo':       'OS',
            'descricao':  os.tipo_servico.nome,
            'valor':      str(os.preco),
            'data':       os.data.strftime('%d/%m/%Y %H:%M'),
            'observacao': os.observacao or '',
            'status':     os.get_status_display(),
        })

    return {
        'id':        carro.pk,
        'placa':     carro.placa,
        'modelo':    carro.carro or '',
        'tipo':      carro.get_tipo_display() if carro.tipo else '',
        'cor':       carro.cor or '',
        'ano':       carro.ano or '',
        'cliente':   str(carro.cliente),
        'historico': historico,
    }


def _carro_resumo(carro):
    return {
        'id':     carro.pk,
        'placa':  carro.placa,
        'modelo': carro.carro or carro.placa,
        'tipo':   carro.get_tipo_display() if carro.tipo else '',
        'cor':    carro.cor or '',
    }