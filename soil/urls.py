from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.form_view, name='form'),
    path('output/', views.recommend, name='output'),
]