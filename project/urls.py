from django.urls import path
from . import views
from django.contrib.auth import views as au_views

app_name = 'project'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('user_page/', views.user_page, name='user_page'),

    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.about_new_game,
         name='material'),
    path('all_news/', views.all_news, name='all_news'),
    path('<int:month>/<int:year>/<slug:slug>/',
         views.about_news,
         name='about_news'),
    path('like/', views.like_post, name="like_post"),
    path('register_done/', views.register_done, name="register_done"),

    path('about_old_game/<int:year>/<int:day>/<slug:slug>/', views.about_old_game, name='about_old_game'),
    path('login/', au_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', au_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('registration/', views.register, name='registration'),
    path('profile/', views.view_profile, name='profile'),
]
