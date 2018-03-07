from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, DateTimeField, ExpressionWrapper
from django.utils import timezone

import datetime

from .models import Task
# Create your views here.

class PriorityTaskView(generic.DetailView):
    template_name = 'todo/index.html'
    model = Task
    
    def getMostImportantTask(self):
        unfinishedTasks = Task.objects.filter(done=False)
        if(unfinishedTasks.exists()):
            tasks = unfinishedTasks.annotate(
            priority= ExpressionWrapper(
            (F('importance') * (timezone.now() - F('dateAdded')))
            + (datetime.timedelta(hours=1) * F('duration')),
            output_field = DateTimeField()
            )).order_by('-priority')

            return tasks[0]
        else:
            return None
    
    def get_object(self):
        try:
            t = self.getMostImportantTask()
        except (Task.DoesNotExist, IndexError) as error:
            t = None
        return t  

        
class TaskAddView(generic.edit.CreateView, SuccessMessageMixin):
    model = Task
    success_url = '/todo'
    success_message = "Task \"%(title)s\" successfully added"
    fields = ['title', 'notes', 'importance', 'duration']
    
    
class TaskEditView(generic.edit.UpdateView):
    model= Task
    success_url = '/todo'
    template_name_suffix = '_edit_form'
    fields = ['title', 'notes', 'importance', 'duration']

    
class TaskDeleteView(generic.edit.DeleteView):
    model = Task
    success_url = '/todo'

def completeTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    try:
        task.done= True
        task.save()
        return HttpResponseRedirect('/todo')
    except (Task.DoesNotExist, KeyError):
        render(request, 'todo/', {"message":"Task not found"})
        