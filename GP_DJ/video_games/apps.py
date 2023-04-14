from django.apps import AppConfig


class VideoGamesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_games'
    verbose_name = 'Видеоигры' # русификация имени приложения в админ панели
