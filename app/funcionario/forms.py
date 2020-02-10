from django import forms
from django.forms import ModelForm
from .models import Funcionario, Plantao, Folga, PlantaoExtra


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('nome', 'sobrenome', 'extra', 'turno')


class FuncionarioUpdate(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('nome', 'sobrenome', 'extra', 'turno')


class PlantaoForm(forms.ModelForm):
    class Meta:
        model = Plantao
        fields = ('turno',)


class FolgaForm(forms.ModelForm):
    class Meta:
        model = Folga
        fields = ('data', 'plantao',)


class PlantaoExtraForm(forms.ModelForm):
    class Meta:
        model = PlantaoExtra
        fields = ('data', 'plantao',)
