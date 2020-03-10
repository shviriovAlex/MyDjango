from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth import authenticate, login
from .forms import CommentForm
from django.http import HttpResponse
from . import forms
from django.contrib.auth.models import User


# Create your views here.

def base(request):
    news_list = models.NewsGame.objects.all()
    return render(request,
                  'includes/all_news.html',
                  {"news_game": news_list})


def materials_details(request, year, month, day, slug):
    all_news = get_object_or_404(models.NewsGame,
                                 slug=slug,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 )
    comments = all_news.comments.filter(active=True)
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
                  'includes/news_game.html',
                  {'news': all_news,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


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
    return render(request, "material/create_material.html", {'form': material_form})


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
                    return HttpResponse('Auth success')
                else:
                    HttpResponse('Inactive user')
            else:
                return HttpResponse('invalid credentials')
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})

