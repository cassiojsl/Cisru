from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('cad_func/', cad_func, name='cad_func'),
    path('listar_func/', listar_func, name='listar_func'),
    path('listar_func/apagar/<str:id>', apagar_func, name='apagar_func'),
    path('listar_func/update_func/<str:nome>', update_func, name='update_func'),
    path('escala_mes/', escala_mes, name='escala_mes'),
    path('cad_plantao', PlantaoView.as_view(), name='cad_plantao'),
    path('plantao_dia', PlantaoDiaView.as_view(), name='plantao_dia'),
    path('apagar_plantao/<str:data>', apagar_plantao, name='apagar_plantao'),
    path('pdf', pdf_view, name='pdf'),
    path('cad_folga', FolgaView.as_view(), name='cad_folga'),
    path('cad_plantao_extra', PlantaoExtraView.as_view(), name='cad_plantao_extra'),
    path('cadastro', cadastro, name="cadastro"),
]
