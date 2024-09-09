from django.shortcuts import HttpResponse

def welcome(request):
    return HttpResponse('<h1>Bienvenue sur mon site</h1>')