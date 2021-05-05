from django.db import models
from django.db.models.deletion import CASCADE

class Event(models.Model):

    name = models.CharField(max_length=100)
    event_date = models.DateField(auto_now=False, auto_now_add=False)
    event_time = models.TimeField(auto_now=False, auto_now_add=False)
    game = models.ForeignKey('Game', on_delete=CASCADE,)
    host = models.ForeignKey('Gamer', on_delete=CASCADE,)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")