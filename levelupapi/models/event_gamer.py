from django.db import models
from django.db.models.deletion import CASCADE

class EventGamer(models.Model):
    event = models.ForeignKey('Event', on_delete=CASCADE)
    gamer = models.ForeignKey('Gamer', on_delete=CASCADE)
