from django.shortcuts import render
from django.http import HttpResponse

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ExpeditionApp.forms import ExpeditionForm
from .models import Expedition

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return HttpResponse("<h1>welcome to ...</h1>")

def welcome(request, name, last_name):
    return HttpResponse(f"Hello a9wa {name} {last_name}!!")

def listExpeditions(request):
    #liste = Expedition.objects.all()
    liste = Expedition.objects.filter(statut="publiee").order_by("date_souhaitee")
    return render(request, 'expedition/list.html', {"list": liste})

def detailsExpedition(request, id):
    expedition = Expedition.objects.get(reference=id)
    return render(request, 'expedition/details.html', {'expedition': expedition})

def deleteExpedition(request, id):
    expedition = Expedition.objects.get(reference=id)
    expedition.delete()
    return HttpResponse(f"Expedition {id} deleted successfully.")





class Liste_exprditions (ListView):
    model = Expedition
    template_name = 'expedition/list.html'
    context_object_name = 'liste'

class Detaille_expedition(DetailView):
    model = Expedition
    template_name = 'expedition/details.html'
    context_object_name = 'expedition'
    
class Delete_expedition(DeleteView):
    model = Expedition
    template_name = 'expedition/delete.html'
    success_url = reverse_lazy('listview_expeditions') # Redirige vers la liste après la suppression

class Create_expedition(CreateView):
    model = Expedition
    template_name = 'expedition/forms.html'
    #fields = '__all__'
    form_class = ExpeditionForm
    success_url = reverse_lazy('listview_expeditions') # Redirige vers la liste après la création

class Update_expedition(LoginRequiredMixin, UpdateView):
    model = Expedition
    template_name = 'expedition/forms.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('listview_expeditions') # Redirige vers la liste après la mise à jour