import os
import django

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecajato.settings')
django.setup()

from django.contrib.auth.models import User

def criar():
    username = 'master'
    password = 'master123'
    email = 'master@email.com'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Usuario {username} criado com sucesso!")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✅ Senha do usuario {username} atualizada!")

if __name__ == "__main__":
    criar()