import os
import django

# Define as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecajato.settings')

try:
    django.setup()
    from django.contrib.auth.models import User
    
    username = 'master'
    password = 'master123'
    email = 'master@email.com'

    # get_or_create evita erros se o usuário já existir
    user, created = User.objects.get_or_create(username=username)
    
    user.set_password(password)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.save()

    if created:
        print(f"✅ SUCESSO: Usuario '{username}' criado do zero!")
    else:
        print(f"✅ SUCESSO: Dados do usuario '{username}' atualizados!")

except Exception as e:
    # Isso vai imprimir o erro exato no log do Railway se algo falhar
    print(f"❌ ERRO CRÍTICO NO SCRIPT: {str(e)}")