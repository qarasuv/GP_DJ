# Generated by Django 4.2 on 2023-04-12 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='video_games_dev_logo/')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='video_games_genre_logo/')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=24, verbose_name='Тип')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='video_games_platform_logo/')),
                ('about', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Платформа',
                'verbose_name_plural': 'Платформы',
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('year', models.IntegerField(default=0)),
                ('rating', models.FloatField(default=5.0)),
                ('views', models.IntegerField(default=0)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='video_games_posters/')),
                ('plot', models.FileField(blank=True, null=True, upload_to='video_games_plots/')),
                ('trailer', models.CharField(blank=True, max_length=11, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('developer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game', to='video_games.developer')),
                ('fans', models.ManyToManyField(blank=True, related_name='favs', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(blank=True, related_name='game', to='video_games.genre')),
                ('platform', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game', to='video_games.platform')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='video_games.game')),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ava', models.ImageField(upload_to='video_games_avas/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='addon', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]