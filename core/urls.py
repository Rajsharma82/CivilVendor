from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('', home, name='home'),
    path('status/', home2, name='status'),
    path('contact/', home3, name='contact'),
    path('hola/', hola, name='hola'),
    path('search/', main, name='search'),
    path('contact_view/', contact_view, name='contact_view'),
    path('genpdf/', generate_pdf, name='genpdf'),
    # Other URL patterns... 
]