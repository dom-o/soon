from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, DateTimeField, ExpressionWrapper
from django.utils import timezone
from django.views import View

import datetime

from .models import Task
# Create your views here.

def getHome(request):
    if request.user.is_authenticated:
        return redirect('todo:task')
    else:
        return redirect('todo:about')

class AboutView(View):
    def get(self, request):
        return render(request, 'todo/about.html')

class PriorityTaskView(LoginRequiredMixin, generic.DetailView):
    template_name = 'todo/task.html'
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

        
class TaskAddView(LoginRequiredMixin, generic.edit.CreateView, SuccessMessageMixin):
    model = Task
    success_url = reverse_lazy('todo:home')
    success_message = "Task \"%(title)s\" successfully added"
    fields = ['title', 'notes', 'importance', 'duration']
    
    
class TaskEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model= Task
    success_url = reverse_lazy('todo:home')
    template_name_suffix = '_edit_form'
    fields = ['title', 'notes', 'importance', 'duration']

    
class TaskDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Task
    success_url = reverse_lazy('todo:home')

def completeTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    try:
        task.done= True
        task.save()
        return redirect('todo:home')
    except (Task.DoesNotExist, KeyError):
        render(request, reverse_lazy('todo:home'), {"message":"Task not found"})
        