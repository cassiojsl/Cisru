# Generated by Django 2.2 on 2019-12-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0004_auto_20191227_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='turno',
            field=models.CharField(default='NDA', max_length=50),
        ),
    ]
