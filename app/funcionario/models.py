from django.db import models
from multiselectfield import MultiSelectField


class Funcionario(models.Model):
    EXTRAS_CHOICES = (
        ('Folguista', 'Folguista'),
        ('Feirista', 'Feirista'),
    )
    nome = models.CharField(max_length=50, null=False, blank=False)
    sobrenome = models.CharField(max_length=50, null=False, blank=False)
    extra = models.CharField(max_length=15, blank=True, choices=EXTRAS_CHOICES)
    turno = models.CharField(max_length=50, default=True)
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'turno']


class Plantao(models.Model):
    turno = models.CharField(max_length=20, primary_key=True, choices=(
        ("NDA", "NDA"),
        ("Madrugada - A", "Madrugada - A"),
        ("Manhã - B", "Manhã - B"),
        ("Tarde - C", "Tarde - C"),
        ("Noite - D", "Noite - D"),
    ),)
    funcionario = models.ManyToManyField(Funcionario)
    REQUIRED_FIELDS = ['turno']


class Folga(models.Model):
    data = models.DateField(primary_key=True)
    plantao = models.ForeignKey(
        "Plantao", on_delete=models.DO_NOTHING, related_name='plantao_folga')

    def get_year(self):
        return self.data.year

    def get_mes(self):
        return self.data.month


class PlantaoExtra(models.Model):
    data = models.DateField(primary_key=True)
    plantao = models.ForeignKey(
        "Plantao", on_delete=models.DO_NOTHING, related_name='plantao_extra')

    def get_year(self):
        return self.data.year

    def get_mes(self):
        return self.data.month
