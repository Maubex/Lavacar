import os
import django
import sys

# Garante que o log apareça imediatamente no Railway
sys.stdout.reconfigure(line_buffering=True)

print("--- INICIANDO SCRIPT DE CRIACAO DE USUARIO ---")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecajato.settings')

try:
    django.setup()
    from django.contrib.auth.models import User
    
    username = 'master'
    password = 'master123'
    
    print(f"Buscando usuario: {username}...")
    user, created = User.objects.get_or_create(username=username)
    
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    if created:
        print("✅ SUCESSO: Usuario MASTER criado do zero!")
    else:
        print("✅ SUCESSO: Senha do MASTER atualizada!")

except Exception as e:
    print(f"❌ ERRO NO DJANGO SETUP OU SCRIPT: {str(e)}")

print("--- FIM DO SCRIPT ---")