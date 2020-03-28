from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from django.views.generic import TemplateView, ListView, RedirectView
from . import forms
from django.contrib.auth.models import User, auth
from . import models
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect


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
    is_liked = False
    if news.likes.filter(id=request.user.id).exists():
        is_liked = True
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
                   'comment_form': comment_form,
                   'is_liked': is_liked,
                   'total_likes': news.total_likes()},
                  )


def like_post(request):
    post = get_object_or_404(models.NewsGame, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


def user_page(request):
    user_now = User.objects.first()
    return render(request,
                  'includes/user_page.html',
                  {"user": user_now})


@login_required
def view_profile(request):
    return render(request, 'registration/profile.html',
                  {'user': request.user})


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
                  'logout.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2 and len(password1) != 0:
            if User.objects.filter(username=username).exists():
                print('Username taken')
            elif User.objects.filter(email=email).exists():
                print('Email taken')
            else:
                user = User.objects.create_user(username=username,
                                                password=password1,
                                                first_name=first_name,
                                                email=email, )
                new_user = user.save()
                print('user created')
                return render(request, 'register_done.html', {'new_user': new_user})

        else:
            print('password not matching')
        return redirect('/registration/')
    else:
        return render(request, 'registration.html')


def register_done(request):
    return render(request, 'register_done.html')
