from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('user_page/', views.user_page, name='user_page' ),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.materials,
         name='material'),
]
