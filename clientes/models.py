from django.db import models

class Cliente(models.Model):
    nome      = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email     = models.EmailField(max_length=100)
    cpf       = models.CharField(max_length=14, null=True, blank=True)
    telefone  = models.CharField(max_length=15, null=True, blank=True)

    # Endereço
    cep    = models.CharField(max_length=9,   null=True, blank=True)
    rua    = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=10,  null=True, blank=True)
    bairro = models.CharField(max_length=50,  null=True, blank=True)
    cidade = models.CharField(max_length=50,  null=True, blank=True)
    estado = models.CharField(max_length=2,   null=True, blank=True)

    def __str__(self) -> str:
        return self.nome

class Carro(models.Model):
    carro    = models.CharField(max_length=50)
    placa    = models.CharField(max_length=8)
    ano      = models.IntegerField()
    cliente  = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.carro