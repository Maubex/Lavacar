from django.urls import path
from . import views

urlpatterns = [
    # Tela principal de atendimento
    path('',
         views.servicos_home,
         name='servicos_home'),

    # Endpoint AJAX de busca
    path('buscar/',
         views.servicos_buscar,
         name='servicos_buscar'),

    # Retorna JSON de um carro específico
    path('carro/<int:carro_pk>/json/',
         views.servicos_carro_json,
         name='servicos_carro_json'),

    # Cadastro rápido de carro
    path('cadastrar-carro/',
         views.servicos_cadastrar_carro,
         name='servicos_cadastrar_carro'),

    # Busca preço por carro + serviço (AJAX)
    path('buscar-preco/',
         views.buscar_preco,
         name='buscar_preco'),

    # Nova Ordem de Serviço
    path('carro/<int:carro_pk>/nova/',
         views.nova_ordem,
         name='nova_ordem'),

    # Compatibilidade com URL antiga
    path('form_lavagem/<int:carro_pk>/',
         views.nova_ordem,
         name='form_lavagem'),
]