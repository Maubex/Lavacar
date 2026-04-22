from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect


def perfil_required(*perfis):
    """
    Decorator que verifica se o usuário está logado e tem o perfil necessário.
    Perfis: 'admin', 'gerente', 'funcionario'
    
    Uso:
        @perfil_required('admin', 'gerente')
        def minha_view(request): ...
    """
    def check_perfil(user):
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=perfis).exists()

    def decorator(view_func):
        @login_required(login_url='login')
        def wrapped(request, *args, **kwargs):
            if check_perfil(request.user):
                return view_func(request, *args, **kwargs)
            return redirect('servicos_home')
        return wrapped
    return decorator


def get_perfil(user):
    """Retorna o perfil do usuário."""
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='gerente').exists():
        return 'gerente'
    if user.groups.filter(name='funcionario').exists():
        return 'funcionario'
    return None