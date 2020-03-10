from django.urls import path
from . import views

urlpatterns = [
    path('1/', views.my_login, name='index'),
    path('register/', views.register, name='register')
]
