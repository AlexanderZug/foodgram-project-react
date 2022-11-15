from __future__ import annotations

from typing import Union

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("email address"),
        max_length=254,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким адресом "
            "электронной почты уже существует.",
        },
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Пользователь с таким именем уже существует."),
        },
    )
    follower: Union[Follow, Manager]
    following: Union[Follow, Manager]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
