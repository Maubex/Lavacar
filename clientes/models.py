from django.db import models


class Cliente(models.Model):
    nome      = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email     = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    cpf       = models.CharField(max_length=14,  unique=True, null=True, blank=True)
    telefone  = models.CharField(max_length=15,  unique=True, null=True, blank=True)
    cep       = models.CharField(max_length=9,   null=True, blank=True)
    rua       = models.CharField(max_length=100, null=True, blank=True)
    numero    = models.CharField(max_length=10,  null=True, blank=True)
    bairro    = models.CharField(max_length=50,  null=True, blank=True)
    cidade    = models.CharField(max_length=50,  null=True, blank=True)
    estado    = models.CharField(max_length=2,   null=True, blank=True)

    class Meta:
        verbose_name        = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering            = ['nome', 'sobrenome']

    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome}'


class Carro(models.Model):

    TIPO_CHOICES = [
        ('hatch',       'Hatch'),
        ('sedan',       'Sedan'),
        ('suv',         'SUV'),
        ('caminhonete', 'Caminhonete'),
        ('moto',        'Moto'),
        ('van',         'Van'),
        ('pickup',      'Pickup'),
        ('esportivo',   'Esportivo'),
        ('outro',       'Outro'),
    ]

    COR_CHOICES = [
        ('preto',    'Preto'),
        ('branco',   'Branco'),
        ('prata',    'Prata'),
        ('cinza',    'Cinza'),
        ('vermelho', 'Vermelho'),
        ('azul',     'Azul'),
        ('verde',    'Verde'),
        ('amarelo',  'Amarelo'),
        ('outro',    'Outro'),
    ]

    # Campo "modelo" foi removido — era órfão (não usado em nenhum formulário ou view).
    # Se precisar no futuro, basta adicionar de volta e rodar makemigrations.
    carro   = models.CharField(max_length=50)
    placa   = models.CharField(max_length=8, unique=True)
    ano     = models.IntegerField(null=True, blank=True)
    tipo    = models.CharField(max_length=20, choices=TIPO_CHOICES, null=True, blank=True)
    cor     = models.CharField(max_length=20, choices=COR_CHOICES,  null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='carros')

    class Meta:
        verbose_name        = 'Carro'
        verbose_name_plural = 'Carros'
        ordering            = ['carro']

    def __str__(self) -> str:
        return f'{self.carro} — {self.placa}'