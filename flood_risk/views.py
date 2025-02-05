from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World!")

def consult_Form(request):
    return render(request, 'consultForm.html')