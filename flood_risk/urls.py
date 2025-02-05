from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('consult_Form/', views.consult_Form, name='consult_Form'),
]