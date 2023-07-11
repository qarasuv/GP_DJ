from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework import generics
from .serializers import *
from .forms import *
from .utils import DataMixin


class IndexListView(ListView):
    model = Game
    template_name = 'video_games/index.html'
    queryset = Game.objects.order_by('-rating')[:8].select_related('platform')
    context_object_name = 'best_games'


class GameListView(ListView):
    paginate_by = 5
    model = Game
    queryset = Game.objects.order_by('year').select_related('platform')
    context_object_name = 'all_games'  # имя в шаблоне ( по умолчанию object_list )


class GameDetailView(DetailView):
    model = Game
    queryset = Game.objects.select_related('platform', 'developer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # comments = cache.get('comments')
        # if not comments:
        context["comments_list"] = Game.objects.get(slug=self.kwargs['slug']).comments.all().select_related('author', 'author__addon')
        # cache.set('comments', comments, 60)
        return context

    def get_object(self, queryset=None):
        game = super(GameDetailView, self).get_object(queryset=queryset)
        game.views += 1
        game.save()
        return game


class GenreListView(ListView):
    model = Genre
    context_object_name = 'genres'
    queryset = Genre.objects.all().prefetch_related('game')


class GenreDetailView(DetailView):
    model = Genre
    extra_context = {
        'genres_all': Genre.objects.all(),
    }


class PlatformListView(ListView):
    model = Platform
    context_object_name = 'platforms'


class PlatformDetailView(DetailView):
    model = Platform


def user_logout(request):
    logout(request)
    return redirect('video_games:login-page')


def search(request):
    match = request.POST.get('match')
    if match:
        games = Game.objects.filter(name__icontains=match).prefetch_related('genre')
        context = {
            'match': match,
            'games': games,
        }
        return render(request, template_name='video_games/search.html',
                      context=context)
    else:
        return redirect('video_games:index')


def add_comment(request):
    text = request.POST.get('text')
    author = request.user
    game_id = request.POST.get('post_id')
    game = Game.objects.get(pk=game_id)
    if text and author:
        new_comment = Comment(text=text, author=author, game=game)
        new_comment.save()
    return HttpResponseRedirect(game.get_absolute_url())


def change_fav_status(request, pk):
    user = request.user
    game = Game.objects.get(pk=pk)
    if user in game.fans.all():
        game.fans.remove(user)
    else:
        game.fans.add(user)
    return HttpResponseRedirect(game.get_absolute_url())


class GameListAPIView(generics.ListAPIView):
    serializer_class = GameSerializer1
    queryset = Game.objects.order_by('name')


def settings(request):
    context = {
        'gf': GameForm(),
        'pf': PlatformForm(),
        'gef': GenreForm(),
        'df': DeveloperForm(),
    }
    return render(request, template_name='video_games/settings.html', context=context)


class AddGame(CreateView):
    form_class = GameForm


class AddPlatform(CreateView):
    form_class = PlatformForm


class AddGenre(CreateView):
    form_class = GenreForm
    # success_url = reverse_lazy('video_games:genre-list')


def add_developer(request):
    form = DeveloperForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('video_games:index')
    else:
        return redirect('video_games:settings')


def pageNotFound(request, exception):  # срабатывает при ошибке 404
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'video_games/register.html'
    success_url = reverse_lazy('video_games:login-page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('video_games:index')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'video_games/login.html'

    def get_success_url(self):
        return reverse_lazy("video_games:index")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'video_games/contacts.html'
    success_url = reverse_lazy('video_games:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context  # dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('video_games:index')
