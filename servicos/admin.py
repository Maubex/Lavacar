from django.contrib import admin
from .models import CategoriaVeiculo, TipoServico, TabelaPreco, Adicional, OrdemServico


@admin.register(CategoriaVeiculo)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']


@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'ativo']
    list_filter  = ['ativo']


@admin.register(TabelaPreco)
class TabelaPrecoAdmin(admin.ModelAdmin):
    list_display = ['tipo_servico', 'categoria_veiculo', 'preco']
    list_filter  = ['tipo_servico', 'categoria_veiculo']


@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'ativo']
    list_filter  = ['ativo']


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display      = ['carro', 'tipo_servico', 'preco', 'status', 'data']
    list_filter       = ['status', 'tipo_servico']
    filter_horizontal = ['adicionais']
    readonly_fields   = ['data']