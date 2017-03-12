from __future__ import unicode_literals

from django.db import models

class Story(models.Model):
    story_id = models.BigIntegerField(primary_key=True)
    author = models.ForeignKey('Author')
    title = models.CharField(max_length=255)
    published = models.DateField()
    updated = models.DateField()
    chapters = models.IntegerField()
    rated = models.CharField(max_length=15)
    language = models.CharField(max_length=15)
    genre1 = models.CharField(max_length=15, default=None, null=True, blank=True)
    genre2 = models.CharField(max_length=15, default=None, null=True, blank=True)
    character1 = models.CharField(max_length=63, default=None, null=True, blank=True)
    character2 = models.CharField(max_length=63, default=None, null=True, blank=True)
    character3 = models.CharField(max_length=63, default=None, null=True, blank=True)
    character4 = models.CharField(max_length=63, default=None, null=True, blank=True)
    reviews = models.IntegerField()

class Author(models.Model):
    author_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    favorite_stories = models.ManyToManyField('Story', blank=True, related_name='+')
    favorite_authors = models.ManyToManyField('self', blank=True, related_name='+')

