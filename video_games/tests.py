from django.test import TestCase
from .models import *


class PlatformTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Platform.objects.create(type='apple')

    def test_1(self):
        platform = Platform.objects.get(id__exact=1)
        s1 = str(platform)
        s2 = platform.type
        self.assertEqual(s1, s2)


class GameTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            name = f'Mafia{i}'
            year = f'100{i}'
            slug = f'{name}-{year}'
            Game.objects.create(name=name, year=year, slug=slug)

    def test_1(self):
        game = Game.objects.get(id__exact=1)
        s1 = f'{game.name}-{game.year}'
        s2 = game.slug
        self.assertEqual(s1, s2)

    def test_2(self):
        all_game = Game.objects.all().count()
        self.assertEqual(all_game, 10)

    # def test_3(self):
    #     resp = self.client.get(reverse('video_games:game-detail', kwargs={'slug': self.slug}))
    #     self.assertTemplateUsed(resp, 'video_games/game_detail.html')

    def test_4(self):
        resp = self.client.get(reverse('video_games:game-list'))
        self.assertEqual(resp.status_code, 200)
