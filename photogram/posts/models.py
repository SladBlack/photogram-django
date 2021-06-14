from django.db import models
from django.contrib.auth.models import User

from .services import TAG_CHOICES


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
    view_count = models.IntegerField(default=0)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, blank=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Post, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return "/post/%i/update" % self.pk

    def __str__(self):
        return str(self.author)

