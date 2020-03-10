from django.shortcuts import render, get_object_or_404
from . import models
from . import forms
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView


def main_page(request):
    many = models.MainPage.objects.all()
    main = models.MainPage.objects.all()
    query = request.GET.get("q")
    if query:
        main = main.filter(title__icontains=query)
    return render(request,
                  'main_page.html',
                  {"base": main})


def materials(request, year, month, day, slug):
    material = get_object_or_404(models.MainPage,
                                 slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 )

    return render(request,
                  'includes/about_game.html',
                  {'material': material})


def user_page(request):
    user_now = User.objects.first()
    return render(request,
                  'includes/user_page.html',
                  {"user": user_now})
