from django.db import models
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.models import User

import datetime
from .priority import getPriority


# Create your models here.
class Task(models.Model):
    done = models.BooleanField(default=False)
    title = models.CharField(max_length=100, help_text='What do you have to get done?')
    notes = models.TextField(max_length=500, blank=True, help_text='Add anything related to this task here')
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
        choices=priorities, default=EVENTUALLY, help_text = 'When do you have to do it?'
    )
    
    BIG=3
    MEDIUM=2
    SMALL=1
    times = (
        (BIG, 'Many hours'),
        (MEDIUM, 'Up to several hours'),
        (SMALL, 'Less than 1 hour'),
    )
    duration = models.IntegerField(
        choices=times, default=MEDIUM, help_text='How long will it take?'
    )
    
    def __str__(self):
        return self.title + " - "+  str(self.getPriority())
    
    @property
    def priority(self):
        return getPriority(self.importance, self.duration, self.dateAdded, timezone.now())
    
    class Meta:
        ordering = ['done', getPriority(F('importance'), F('duration'), F('dateAdded'), timezone.now()).desc()]