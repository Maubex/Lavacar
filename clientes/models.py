from django.db import models

class Cliente(models.Model):
    nome      = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email     = models.EmailField(max_length=100, null=True, blank=True)
    cpf       = models.CharField(max_length=14, null=True, blank=True)
    telefone  = models.CharField(max_length=15, null=True, blank=True)
    cep       = models.CharField(max_length=9,   null=True, blank=True)
    rua       = models.CharField(max_length=100, null=True, blank=True)
    numero    = models.CharField(max_length=10,  null=True, blank=True)
    bairro    = models.CharField(max_length=50,  null=True, blank=True)
    cidade    = models.CharField(max_length=50,  null=True, blank=True)
    estado    = models.CharField(max_length=2,   null=True, blank=True)

    def __str__(self) -> str:
        return self.nome


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

    carro   = models.CharField(max_length=50)
    modelo  = models.CharField(max_length=50, null=True, blank=True)
    placa   = models.CharField(max_length=8)
    ano     = models.IntegerField(null=True, blank=True)
    tipo    = models.CharField(max_length=20, choices=TIPO_CHOICES, null=True, blank=True)
    cor     = models.CharField(max_length=20, choices=COR_CHOICES, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.carro