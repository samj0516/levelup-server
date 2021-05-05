from django.db import models
from django.db.models.deletion import DO_NOTHING

class Game(models.Model):

    name = models.CharField(max_length=50)
    max_players = models.IntegerField(null=True)
    min_players = models.IntegerField(null=True)
    difficulty_level = models.IntegerField(null=True)
    type = models.ForeignKey('GameType', on_delete=models.DO_NOTHING, null=True)

