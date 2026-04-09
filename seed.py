import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecajato.settings')
django.setup()

from django.contrib.auth.models import User
from servicos.models import TipoServico, CategoriaVeiculo, TabelaPreco

# 1. CRIAR USUÁRIO ADMIN (Versão automática para o Railway não travar)
def criar_admin():
    username = 'admin'
    password = 'admin123'
    email = 'renan.buosi@hotmail.com'
    
    # Busca o usuário ou cria um novo se não existir
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    
    # Define/Reseta a senha e garante os poderes de admin
    user.set_password(password) # Isso criptografa a senha corretamente
    user.is_superuser = True
    user.is_staff = True
    user.save()

    if created:
        print(f'👤 Usuário admin CRIADO: {username} / {password}')
    else:
        print(f'👤 Senha do admin RESETADA: {username} / {password}')

# 2. CRIAR CATEGORIAS E SERVIÇOS (Seu código original mantido)
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
        try:
            servico = TipoServico.objects.get(nome=servico_nome)
            categoria = CategoriaVeiculo.objects.get(nome=categoria_nome)
            TabelaPreco.objects.get_or_create(
                tipo_servico=servico,
                categoria_veiculo=categoria,
                defaults={'preco': valor}
            )
        except Exception as e:
            print(f"Erro ao inserir preço para {servico_nome}: {e}")

    print('✅ Dados de serviços e preços importados!')

if __name__ == "__main__":
    criar_admin()
    popular_dados()