from django.urls import path
from . import views
from django.contrib.auth import views as au_views
app_name = 'project_1'
urlpatterns = [
    path('', views.base, name='base'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.materials_details,
         name='material_details'),
    path('login/', au_views.LoginView.as_view(), name='login'),
    path('logout/', au_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', au_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', au_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', au_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', au_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]