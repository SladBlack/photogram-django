from django.db import models
from django.contrib.auth.models import User


class ImageQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.image.delete()
        super(ImageQuerySet, self).delete(*args, **kwargs)


class Post(models.Model):
    objects = ImageQuerySet.as_manager()
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.CASCADE,
                               verbose_name='Пользователь')
    image = models.ImageField(upload_to='images/')

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Post, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.author)
