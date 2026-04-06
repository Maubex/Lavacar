from django.db import models
from clientes.models import Carro


class CategoriaVeiculo(models.Model):
    """
    Veículo Pequeno, Médio, SUV Grande, Grande
    """
    nome      = models.CharField(max_length=50, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Exemplos de carros')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria de Veículo'
        verbose_name_plural = 'Categorias de Veículo'


class TipoServico(models.Model):
    """
    Ducha, Lavar e Secar, Completa 1, Completa 2
    """
    nome      = models.CharField(max_length=50, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    ativo     = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Serviço'
        verbose_name_plural = 'Tipos de Serviço'


class TabelaPreco(models.Model):
    """
    Relaciona tipo de serviço + categoria de veículo = preço
    Ex: Ducha + Pequeno = R$25,00
    """
    tipo_servico      = models.ForeignKey(TipoServico,      on_delete=models.CASCADE, verbose_name='Serviço')
    categoria_veiculo = models.ForeignKey(CategoriaVeiculo, on_delete=models.CASCADE, verbose_name='Categoria')
    preco             = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço (R$)')

    def __str__(self):
        return f'{self.tipo_servico} — {self.categoria_veiculo} — R${self.preco}'

    class Meta:
        verbose_name = 'Tabela de Preço'
        verbose_name_plural = 'Tabela de Preços'
        unique_together = ['tipo_servico', 'categoria_veiculo']


class Adicional(models.Model):
    """
    Serviços extras — ex: cera, pretinho, aromatizante
    """
    nome  = models.CharField(max_length=50, verbose_name='Nome')
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço (R$)')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Adicional'
        verbose_name_plural = 'Adicionais'


class OrdemServico(models.Model):
    """
    Registro de um atendimento
    """
    STATUS_CHOICES = [
        ('aguardando',   'Aguardando'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado',   'Finalizado'),
    ]

    carro        = models.ForeignKey(Carro,       on_delete=models.CASCADE, related_name='ordens',    verbose_name='Carro')
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.CASCADE,                            verbose_name='Serviço')
    adicionais   = models.ManyToManyField(Adicional, blank=True,                                       verbose_name='Adicionais')
    preco        = models.DecimalField(max_digits=8, decimal_places=2,                                 verbose_name='Preço (R$)')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando',       verbose_name='Status')
    observacao   = models.TextField(blank=True, null=True,                                             verbose_name='Observação')
    data         = models.DateTimeField(auto_now_add=True,                                             verbose_name='Data')

    def __str__(self):
        return f'{self.tipo_servico} — {self.carro.placa}'

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data']