from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from django.views.generic import TemplateView, ListView, RedirectView
from . import forms
from django.contrib.auth.models import User, auth
from . import models
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def main_page(request):
    main = models.MainPage.objects.all()
    query = request.GET.get("q")
    if query:
        main = main.filter(title__icontains=query)
    return render(request,
                  'main_page.html',
                  {"base": main})


def about_new_game(request, year, month, day, slug):
    material = get_object_or_404(models.MainPage,
                                 slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 )

    return render(request,
                  'includes/about_new_game.html',
                  {'material': material})


def all_games(request):
    games = models.Games.objects.all()
    return render(request,
                  'includes/all_games.html',
                  {"games": games})


def about_game(request, slug):
    game = get_object_or_404(models.Games, slug=slug)
    games = models.Games.objects.all()
    return render(request,
                  'includes/about_game.html',
                  {'game': game,
                   'games': games})


def about_old_game(request, year, day, slug):
    games = get_object_or_404(models.OldGames,
                              slug=slug,
                              publish__year=year,
                              publish__day=day,
                              )

    return render(request,
                  'includes/about_old_game.html',
                  {'games': games})


def all_news(request):
    news_list = models.NewsGame.objects.all()
    return render(request,
                  'includes/all_news.html',
                  {"news_list": news_list})


def about_news(request, year, month, slug):
    news = get_object_or_404(models.NewsGame,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             )
    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = all_news
            new_comment.save()
        return redirect(all_news)
    else:
        comment_form = CommentForm()

    return render(request,
                  'includes/about_news.html',
                  {'news': news,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def user_page(request):
    user_now = User.objects.first()
    return render(request,
                  'includes/user_page.html',
                  {"user": user_now})


def create_form(request):
    if request.method == 'POST':
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(" ", "-")
            new_material.save()
            return render(request,
                          'material/detail.html',
                          {'material': new_material})
    else:
        material_form = forms.MaterialForm()
    return render(request, "material/create_material.html",
                  {'form': material_form})


@login_required
def view_profile(request):
    return render(request, 'includes/profile.html', {'user': request.user})


def user_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return main_page(request)
                else:
                    HttpResponse('Inactive user')
            else:
                return HttpResponse('invalid credentials')
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    return render(request,
                  'register/logged_out.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Username taken')
            elif User.objects.filter(email=email).exists():
                print('Email taken')
            else:
                user = User.objects.create_user(username=username,
                                                password=password1,
                                                first_name=first_name,
                                                email=email, )
                user.save()
                print('user created')

        else:
            print('password not matching')
        return redirect('/')
    else:
        return render(request, 'registration.html')
