from django.urls import path
from . import views
from django.contrib.auth import views as au_views

app_name = 'project'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('user_page/', views.user_page, name='user_page' ),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.materials,
         name='material'),
    path('base/', views.base, name='base'),
    path('<int:year>/<int:month>/<slug:slug>/',
         views.materials_details,
         name='material_details'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('password_reset/', au_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', au_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', au_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', au_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.view_profile, name='profile'),
]
