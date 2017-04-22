# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
#from django.template.defaultfilters import slugify


def get_imagep_Runone(instance, filename):
    return '/'.join(['Rundate', instance.slug, filename])


class Runone(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    useredit = models.CharField(max_length=32, blank=True, null=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    image = models.ImageField(upload_to=get_imagep_Runone, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()

        return super(Runone, self).save(*args, **kwargs)


def get_image_path(instance, filename):
    return '/'.join(['run_images', instance.runshow.slug, filename])


class Upload(models.Model):
    runshow = models.ForeignKey(Runone, related_name="uploads")
    image = models.ImageField(upload_to=get_image_path)

    def save(self, *args, **kwargs):
        super(Upload, self).save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image)
            i_width, i_height = image.size
            max_size = (640, 480)

            if i_width > 1000:
                image.thumbnail(max_size, Image.ANTIALIAS)
                image.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Runone, related_name='comments')
    user = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)
