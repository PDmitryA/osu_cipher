from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    email = models.EmailField('email address', blank=True, null=True)

class Score(models.Model):
    class Meta:
        verbose_name = 'Результат игрока'
        verbose_name_plural = 'Результаты игроков'

    user = models.ForeignKey(
        'www.User',
        on_delete=models.CASCADE,
        related_name='user_scores',
        verbose_name='Пользователь'
    )
    score = models.BigIntegerField(verbose_name='Очки')
    created = models.DateTimeField(auto_now_add=True)
