from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from ..coordenador.models import Coordenador
from django.db.models import Q
from .forms import *
from .models import *
from datetime import datetime
from datetime import date
from pytz import timezone
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from .Classes.Funcionario import FuncionarioEscala

timeDate = datetime.now()
month = timeDate.month
ano = timeDate.year
# Create your views here
# cadastro de funcionario
@login_required(login_url='login')
def cad_func(request):
    plantoes = Plantao.objects.all()
    coordenador = Coordenador.objects.get(username=request.user.username)
    func_campos = FuncionarioForm(request.POST)
    if request.method == 'POST' and coordenador.is_authenticated:
        if func_campos.is_valid():
            func_campos.save(commit=False)
            funcionario = Funcionario()
            funcionario.nome = func_campos.cleaned_data['nome']
            funcionario.sobrenome = func_campos.cleaned_data['sobrenome']
            funcionario.extra = func_campos.cleaned_data['extra']
            funcionario.turno = func_campos.cleaned_data['turno']
            funcionario.save()
            plantao = Plantao.objects.get(turno=funcionario.turno)
            plantao.funcionario.add(funcionario)
            plantao.save()
            context = {"plantao":plantoes}
            return render(request, 'funcionario/cad_func.html',context)
        else:
            context = {"plantao":plantoes,"form.errors": func_campos.errors}
            messages.error(request, "Funcionário Não Cadastrado")
            return render(request, 'funcionario/cad_func.html',context)
    else:
        if coordenador.is_authenticated:
            context = {"plantao":plantoes}
            return render(request, "funcionario/cad_func.html",context)
        else:
            return redirect('logout_view')

#lista dos funcionarios cadastrados
@login_required(login_url='login')
def listar_func(request):
    plantao = Plantao.objects.all()
    funcionarios = Funcionario.objects.all()
    coordenador = Coordenador.objects.get(username=request.user.username)
    if coordenador.is_authenticated:
        return render(request, "funcionario/lista_func.html",{"funcionarios":funcionarios,"plantao":plantao})
    else:
        return redirect('logout_view')

#apagar funcionario
@login_required(login_url='login')
def apagar_func(request, id):
    funcionarios = Funcionario.objects.filter(id=id)
    funcionarios.delete()
    funcionarios = Funcionario.objects.all()
    coordenador = Coordenador.objects.get(username=request.user.username)
    if coordenador.is_authenticated:
        return render(request, "funcionario/lista_func.html",{"funcionarios":funcionarios})
    else:
        return redirect('logout_view')

#atualizar cadastro do funcionario // refazer utilizando classe 
@login_required(login_url='login')
def update_func(request, nome):
    funcionarios = Funcionario.objects.filter(nome=nome)
    coordenador = Coordenador.objects.get(username=request.user.username)
    plantao = Plantao.objects.all()
    form = FuncionarioForm()
    if request.method == 'POST' and coordenador.is_authenticated:
        update = FuncionarioUpdate(request.POST, request.FILES)
        if update.is_valid():

            funcionario = Funcionario()
            funcionario.nome = update.cleaned_data['nome']
            funcionario.sobrenome = update.cleaned_data['sobrenome']
            funcionario.extra = update.cleaned_data['extra']
            funcionario.turno = update.cleaned_data['turno']
            funcionario.save()
            return redirect('lista_func')
        else:
            return render(request, "funcionario/update_func.html",{"funcionarios":funcionarios,"plantao":plantao})
    else:
        if coordenador.is_authenticated:
            return render(request,"funcionario/update_func.html",{"funcionarios":funcionarios,"plantao":plantao})
        else:
            return redirect('logout_view')

@login_required(login_url='login')
def escala_mes(request):
    mes = request.GET.get('selected_month')
    global ano
    if mes is None:
        mes = month
    else:
        mes = int(request.GET.get('selected_month'))
    dayNamesMin = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D']
    meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    semana = []
    domingos = []
    dias_mes = getDiasMes(mes)#recebe a quantidade de dias do mes

    for i in range(1,dias_mes):
        dt = datetime(year=ano, month=mes, day=i)
        if (dayNamesMin[dt.weekday()]) == 'D':
            domingos.append(i)
        semana.append(dayNamesMin[dt.weekday()])
    obterTurnodeFolgaDomingo(domingos,dt)
    funcionarios = Funcionario.objects.all()[:11]
    escala_f = []
    for fun in funcionarios:
        f = FuncionarioEscala((fun.nome +" "+fun.sobrenome),fun.turno)
        for i in range(1,dias_mes):
            f.add_escala((fun.turno).split("-")[-1])
        escala_f.append(f)
    func = Folga.objects.all()
    extra = PlantaoExtra.objects.all()
    plantonistas = Funcionario.objects.all()

    getFolgaE(mes)
    for esc_fun in escala_f:
        for i in func:
            plantao = i.plantao
            folga = ((i.data).strftime("%d"))
            mesEscala = int(((i.data).strftime("%m")))   
            x = 0 
            folga = (int(folga)-1)
            while x < (dias_mes):
                x+=1
                if mesEscala == mes:
                    if (plantao.turno == esc_fun.turno):
                        esc_fun.add_folga(folga)
                    for i in extra:
                        plantaExtra = i.plantao
                        diaExtra = ((i.data).strftime("%d"))
                        mesExtra = int(((i.data).strftime("%m")))
                        diaExtra =(int(diaExtra)-1)
                        if mesExtra == mes:
                            if plantaExtra.turno  == esc_fun.turno:
                                esc_fun.add_extra(diaExtra)
    return render(request,"funcionario/escala_mes.html",{"mes":meses[mes-1],"funcionarios":funcionarios,'range': range(1,dias_mes),'semana':semana,'escala':escala_f,"plantonistas":plantonistas,"domingos":domingos})



class PlantaoView(View):
    
    form_class = PlantaoForm
    model = Plantao
    template_name = 'coordenador/cad_plantao.html'
    def get(self, request):
        form = self.form_class()
        context = {"form":form}
        return render(request, self.template_name, context)

    #@login_required(login_url='login')
    def post(self, request):
        #coordenador = Coordenador.objects.get(username=request.user.username)
        form = self.form_class(request.POST)
        if form.is_valid():# and coordenador.is_authenticated:
            form.save()
        
        context = {"form":form}
        return render(request, self.template_name, context)

class FolgaView(ListView):
    
    form_class = FolgaForm
    model = Folga
    template_name = 'coordenador/cad_folga.html'
    def get(self, request):
        form = self.form_class()
        plantao = Plantao.objects.all()
        context = {"form":form,"plantao":plantao}
        return render(request, self.template_name, context)

    #@login_required(login_url='login')
    def post(self, request):
        #coordenador = Coordenador.objects.get(username=request.user.username)
        form = self.form_class(request.POST)
        if form.is_valid():# and coordenador.is_authenticated:
            data = form.cleaned_data['data']
            turno = form.cleaned_data['plantao']
            form.save()
            plantao = Plantao.objects.get(turno=turno.turno)
            dayoff = int(data.strftime("%d").replace("0", ""))
            mes = int(data.strftime("%m").replace("0",""))
            daysTotal = getDiasMes(mes)
            form.save()
            while dayoff <= (daysTotal+1):
                   dayoff +=6
                   if dayoff >(daysTotal+1):
                       break
                   dataNova = datetime.strptime(data.strftime("%Y-%m-"+str(dayoff)) ,"%Y-%m-%d")
                   dataNova = dataNova.strftime("%Y-%m-%d")
                   newfolga = Folga()
                   newfolga.plantao = plantao
                   newfolga.data = dataNova
                   newfolga.save()

        form = self.form_class()
        return self.get(request)

class PlantaoExtraView(View):
    
    form_class = PlantaoExtraForm
    model = PlantaoExtra
    template_name = 'coordenador/cad_plantao_extra.html'
    def get(self, request):
        form = self.form_class()
        plantao = Plantao.objects.all()
        context = {"form":form,"plantao":plantao}
        return render(request, self.template_name, context)

    #@login_required(login_url='login')
    def post(self, request):
        #coordenador = Coordenador.objects.get(username=request.user.username)
        plantaoExtra = self.model.objects.all()
        form = self.form_class(request.POST)
        plantao = Plantao.objects.all()
        if form.is_valid():# and coordenador.is_authenticated
            form.save()
        context = {"form":form}
        return render(request, self.template_name, context)



class PlantaoDiaView(View):

    template_name = 'funcionario/plantao_dia.html'
    def get(self, request):
        plantao = Plantao.objects.all()
        listaPlantao = getTurno(plantao)
        return render(request, self.template_name,{"plantao":listaPlantao})

    #@login_required(login_url='login')
    def post(self, request):
        turno = request.POST.get('plantao')
        data =request.POST.get('month')
        plantao = Plantao.objects.all()
        plantaoExtra = PlantaoExtra.objects.all()
        listaPlantao = getTurno(plantao)
        folga_plantao_e = getFolgaE(int(data))
        plantaofolga = Folga.objects.filter(plantao=turno,data__month__exact=data)
        totalPlantoes = getTotalDayoff(plantaofolga, data)
        return render(request, self.template_name,{"data":data,"plantao":listaPlantao,"plantaofolga":plantaofolga,"turno":turno,"plantaoExtra":plantaoExtra,"folga_plantao_e":folga_plantao_e,"totalPlantoes":totalPlantoes})

@login_required(login_url='login')
def apagar_plantao(request, data):
    plantao = Plantao.objects.all()
    listaPlantao = getTurno(plantao)
    folga = Folga.objects.filter(data=data)
    plantaoExtra = PlantaoExtra.objects.filter(data=data)
    folga.delete()
    plantaoExtra.delete()
    folga = Folga.objects.all()
    coordenador = Coordenador.objects.get(username=request.user.username)
    plantaoExtra = PlantaoExtra.objects.all()
    funcionarios = Funcionario.objects.all()
    
    context = {"folga":folga,"funcionarios":funcionarios,"plantaoExtra":plantaoExtra,}
    if coordenador.is_authenticated:
        return render(request, "funcionario/plantao_dia.html",context)
    else:
        return redirect('logout_view')

def pdf_view(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='escala.pdf')


def getTurno(plantao):
    listaplantao = []
    for p in plantao:
        listaplantao.append(p.turno)
    return listaplantao

def getDiasMes(mes):
    days_of_Month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dias = days_of_Month[mes - 1]
    return dias+1

def getFolgaE(mes=datetime):
    dias_mes = getDiasMes(mes)
    folga = []
    folgas = Folga.objects.all()
    PlaExtra = PlantaoExtra.objects.all()
    dias = []
    for f in folgas:
        d = int(f.data.strftime("%d").replace("0",""))
        if d not in dias:
            dias.append(datetime.strptime(f.data.strftime("%Y-"+str(mes)+"-"+str(d)) ,"%Y-%m-%d"))
            dias.sort()
    for i in range(1,dias_mes):
        folga.append(datetime.strptime(f.data.strftime("%Y-"+str(mes)+"-"+str(i)) ,"%Y-%m-%d"))
    for f in PlaExtra:
        d = int(f.data.strftime("%d").replace("0",""))
        if d not in dias:
            dias.append(datetime.strptime(f.data.strftime("%Y-"+str(mes)+"-"+str(d)) ,"%Y-%m-%d"))
            dias.sort()
    dias_folgas_E = list(set(folga) - set(dias))
    
    return (dias_folgas_E.sort())

def obterTurnodeFolgaDomingo(domingos=[],data=datetime):
    turno_folgas = {}
    #print(data)
    folga = Folga.objects.filter(data__month__exact=data.strftime("%m"))
    #print(folga)
    #print(folga.filter(data__day__exact=domingos))
    #folga = folga.get(data__day__exact=domingo)


def getTotalDayoff(plantaoFolga, mes):
    total = plantaoFolga
    mes = getDiasMes(int(mes))
    totalPlantoes = []
    for plantao in total:
        totalPlantoes.append(plantao.data)
    return ((mes-1)-(len(totalPlantoes)))


#teste - Página Cadastro botões

def cadastro(request):
    return render(request, "funcionario/cadastro.html")