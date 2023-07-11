from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = 'video_games'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    #path('', cache_page(60)(IndexListView.as_view()), name='index'),
    path('game/all/', GameListView.as_view(), name='game-list'),
    path('game/<slug:slug>/', GameDetailView.as_view(), name='game-detail'),
    path('genre/all/', GenreListView.as_view(), name='genre-list'),
    path('genre/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    path('platform/all/', PlatformListView.as_view(), name='platform-list'),
    path('platform/<int:pk>/', PlatformDetailView.as_view(), name='platform-detail'),
    path('user/register/', RegisterUser.as_view(), name='register'),
    path('page/login/', LoginUser.as_view(), name='login-page'),
    path('user/logout/', user_logout, name='user-logout'),
    path('search/', search, name='search'),
    path('add/comment/', add_comment, name='add-comment'),
    path('fav/change/<int:pk>/', change_fav_status, name='fav-status'),
    path('api/v1/gamelist', GameListAPIView.as_view()),
    path('settings/', settings, name='settings'),
    path('add/game/', AddGame.as_view(), name='add-game'),
    path('add/platform/', AddPlatform.as_view(), name='add-platform'),
    path('add/genre/', AddGenre.as_view(), name='add-genre'),
    path('add/developer/', add_developer, name='add-developer'),
]