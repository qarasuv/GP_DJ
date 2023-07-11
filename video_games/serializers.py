from rest_framework import serializers
from .models import *


class GameSerializer1(serializers.ModelSerializer):
    developer = serializers.StringRelatedField()

    class Meta:
        model = Game
        fields = ['name', 'year', 'rating', 'poster', 'developer']
