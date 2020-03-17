from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'easygame/home.html'


class Dashboard(TemplateView):
    template_name = 'easygame/dashboard.html'
