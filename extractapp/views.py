from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse

def firstView(request):
    #process and send reponse
    return HttpResponse('first view response')

