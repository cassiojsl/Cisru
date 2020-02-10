from django.contrib import admin
from django.urls import path
from .views import homecoord, loginCoordenador, logout_view, cad_plantao, cad_folga


urlpatterns = [
    path('', homecoord, name='home'),
    path('login/', loginCoordenador, name='login'),
    path('cad_folga/', cad_folga, name='cad_folga'),
    path('logout_manager/', logout_view, name='logout_manager'),
]
