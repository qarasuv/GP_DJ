from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Platform(models.Model):
    type = models.CharField(max_length=24, verbose_name='Тип')
    logo = models.ImageField(upload_to='video_games_platform_logo/', null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    # game

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('video_games:platform-detail', kwargs={'pk': self.id})

    class Meta:  # для русификации в админ панели
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'
        ordering = ['type']


class Genre(models.Model):
    name = models.CharField(max_length=24)
    logo = models.ImageField(upload_to='video_games_genre_logo/', null=True, blank=True)

    # game

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('video_games:genre-detail', kwargs={'pk': self.id})


class Developer(models.Model):
    name = models.CharField(max_length=24)
    logo = models.ImageField(upload_to='video_games_dev_logo/', null=True, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=128)
    year = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0)
    views = models.IntegerField(default=0)
    poster = models.ImageField(upload_to='video_games_posters/', null=True, blank=True)
    plot = models.FileField(upload_to='video_games_plots/', null=True, blank=True)
    trailer = models.CharField(max_length=11, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    platform = models.ForeignKey(Platform, related_name='game', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    developer = models.ForeignKey(Developer, related_name='game', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='game', blank=True)
    fans = models.ManyToManyField(User, related_name='favs', blank=True)
    # comments

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('video_games:game-detail', kwargs={'slug': self.slug})


class Addon(models.Model):
    user = models.OneToOneField(User, related_name='addon', on_delete=models.CASCADE)
    ava = models.ImageField(upload_to='video_games_avas/')

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('video_games:author', kwargs={'pk': self.user.id})


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='comments', on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-published']
