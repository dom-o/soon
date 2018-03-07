from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class Task(models.Model):
    done = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    notes = models.TextField(max_length=500)
    dateAdded = models.DateTimeField('date added', auto_now_add=True)
    
    NOW=3
    SOON=2
    EVENTUALLY=1
    priorities = (
        (NOW, 'Now'),
        (SOON, 'Soon'),
        (EVENTUALLY, 'Eventually'),
    )
    importance = models.IntegerField(
        choices=priorities, default=EVENTUALLY
    )
    
    BIG=12
    MEDIUM=5
    SMALL=1
    times = (
        (BIG, 'Many hours'),
        (MEDIUM, 'Up to several hours'),
        (SMALL, '<1 hour'),
    )
    duration = models.IntegerField(
        choices=times, default=MEDIUM
    )
    
    def __str__(self):
        return self.title + " - "+  str(self.getPriority())
    
    def getPriority(self):
        return (self.importance * (timezone.now() - self.dateAdded)) + datetime.timedelta(hours=self.duration)
    