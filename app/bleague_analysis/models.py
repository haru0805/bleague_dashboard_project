from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class District(models.Model):
    name = models.CharField(max_length=50,  default="unknown")
    created_at = models.DateTimeField('created_at', default=timezone.now)
    updated_at = models.DateTimeField('updated_at', auto_now=True)


class Team(models.Model):
    bleague_id = models.IntegerField('bleague_id',default=0, primary_key=True)
    name = models.CharField(max_length=50, default="default name")
    location = models.CharField(max_length=50, default='unknown')
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, default=4)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

class Player(models.Model):
    bleague_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50,  default="name")
    number = models.IntegerField(default=0)
    position_id = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

class Game(models.Model):
    date = models.DateField()
    own_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='own_team')
    other_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='other_team')
    own_score = models.IntegerField(default=999)
    other_score = models.IntegerField(default=999)
    win_or_lose = models.IntegerField(default=999)
    home_or_away = models.IntegerField(default=999)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

