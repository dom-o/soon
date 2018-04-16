from django.db import models
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.models import User

import datetime

# Create your models here.
class Task(models.Model):
    done = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    notes = models.TextField(max_length=500, blank=True)
    dateAdded = models.DateTimeField('date added', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    NOW=3
    SOON=2
    EVENTUALLY=1
    priorities = (
        (NOW, 'Now'),
        (SOON, 'Soon'),
        (EVENTUALLY, 'Eventually'),
    )
    importance = models.IntegerField(
        choices=priorities, default=EVENTUALLY, help_text = 'When do you gotta get this done?'
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
        choices=times, default=MEDIUM, help_text='How long will it take?'
    )
    
    def __str__(self):
        return self.title + " - "+  str(self.getPriority())
    
    @property
    def priority(self):
        return (self.importance * (timezone.now() - self.dateAdded)) + datetime.timedelta(hours=self.duration)
    
    class Meta:
        ordering = ['done', ((F('importance') * (timezone.now() - F('dateAdded'))) + (datetime.timedelta(hours=1) * F('duration'))).desc()]