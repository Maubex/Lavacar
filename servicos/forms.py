from django import forms
from .models import Lavagem, Estetica


class LavagemForm(forms.ModelForm):
    class Meta:
        model = Lavagem
        fields = ['tipo', 'valor', 'observacao']
        widgets = {
            'tipo':       forms.Select(attrs={'class': 'form-control'}),
            'valor':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 50.00'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações...'}),
        }


class EsteticaForm(forms.ModelForm):
    class Meta:
        model = Estetica
        fields = ['tipo', 'valor', 'observacao']
        widgets = {
            'tipo':       forms.Select(attrs={'class': 'form-control'}),
            'valor':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 350.00'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações...'}),
        }