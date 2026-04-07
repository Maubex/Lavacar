import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecajato.settings')
django.setup()

from django.contrib.auth.models import User
from servicos.models import TipoServico, CategoriaVeiculo, TabelaPreco

# 1. CRIAR USUÁRIO ADMIN (O que faltava para você logar!)
def criar_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@email.com', 'admin123')
        print('👤 Usuário admin criado: admin / admin123')
    else:
        print('👤 Usuário admin já existe.')

# 2. CRIAR CATEGORIAS E SERVIÇOS
def popular_dados():
    # Categorias
    categorias = ['Veículo Pequeno', 'Veículo Médio', 'Veículo SUV Grande', 'Veículo Grande']
    for cat in categorias:
        CategoriaVeiculo.objects.get_or_create(nome=cat)

    # Tipos de serviço
    servicos = ['Ducha', 'Lavar e Secar', 'Completa 1', 'Completa 2']
    for s in servicos:
        TipoServico.objects.get_or_create(nome=s)

    # Tabela de preços
    precos = [
        ('Ducha', 'Veículo Pequeno', 25), ('Ducha', 'Veículo Médio', 30),
        ('Ducha', 'Veículo SUV Grande', 35), ('Ducha', 'Veículo Grande', 40),
        ('Lavar e Secar','Veículo Pequeno', 40), ('Lavar e Secar','Veículo Médio', 45),
        ('Lavar e Secar','Veículo SUV Grande', 50), ('Lavar e Secar','Veículo Grande', 60),
        ('Completa 1', 'Veículo Pequeno', 65), ('Completa 1', 'Veículo Médio', 70),
        ('Completa 1', 'Veículo SUV Grande', 75), ('Completa 1', 'Veículo Grande', 90),
        ('Completa 2', 'Veículo Pequeno', 75), ('Completa 2', 'Veículo Médio', 80),
        ('Completa 2', 'Veículo SUV Grande', 85), ('Completa 2', 'Veículo Grande', 100),
    ]

    for servico_nome, categoria_nome, valor in precos:
        servico = TipoServico.objects.get(nome=servico_nome)
        categoria = CategoriaVeiculo.objects.get(nome=categoria_nome)
        TabelaPreco.objects.get_or_create(
            tipo_servico=servico,
            categoria_veiculo=categoria,
            defaults={'preco': valor}
        )
    print('✅ Dados de serviços e preços importados!')

if __name__ == "__main__":
    criar_admin()
    popular_dados()