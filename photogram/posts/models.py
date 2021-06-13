from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.CASCADE,
                               verbose_name='Пользователь')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.author)
