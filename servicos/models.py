from django.db import models
from clientes.models import Cliente
from .choices import ChoicesCategoriaManutencao
from datetime import datetime
from secrets import token_hex, token_urlsafe
from decimal import Decimal # Importante para cálculos precisos

class CategoriaManutencao(models.Model):
    # Dica: max_length=3 parece curto se o "titulo" for o nome da categoria. 
    # Se for uma sigla, está ok!
    titulo = models.CharField(max_length=50, choices=ChoicesCategoriaManutencao.choices)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.get_titulo_display() # Mostra o nome legível do Choice

class ServicoAdicional(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField()
    # Mudado para DecimalField por segurança financeira
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.titulo

class Servico(models.Model):
    titulo = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    categoria_manutencao = models.ManyToManyField(CategoriaManutencao)
    servicos_adicionais = models.ManyToManyField(ServicoAdicional, blank=True)
    
    data_inicio = models.DateField(null=True, blank=True)
    data_entrega = models.DateField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    
    # "protocole" corrigido para "protocolo" (opcional)
    protocolo = models.CharField(max_length=52, null=True, blank=True)
    identificador = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.titulo} - {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = datetime.now().strftime("%d%m%Y%H%M%S") + token_hex(8)

        if not self.identificador:
            self.identificador = token_urlsafe(16)

        super(Servico, self).save(*args, **kwargs)

    def preco_total(self):
        # Soma categorias + serviços adicionais
        total = Decimal('0.00')
        
        # Somar Categorias
        for cat in self.categoria_manutencao.all():
            total += cat.preco
            
        # Somar Adicionais
        for add in self.servicos_adicionais.all():
            total += add.preco
            
        return total