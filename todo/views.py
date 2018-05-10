from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F, DateTimeField, ExpressionWrapper
from django.utils import timezone
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

import datetime

from .models import Task
from .priority import getPriority
# Create your views here.

class CreateUserView(View):
    def get(self, request):
        return render(request, 'registration/signup.html', {'form': UserCreationForm()})
        
    def post(self, request):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('todo:home')
        else:
            return render(request, 'registration/signup.html', {'form': form})

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
    
    def get_object(self):
        try:
            mostImportantTask = Task.objects.filter(done=False, user=self.request.user).first()
        except (Task.DoesNotExist, IndexError) as error:
            mostImportantTask = None
        return mostImportantTask

class TaskListView(LoginRequiredMixin, generic.list.ListView):
    model = Task
    paginate_by = 30
    
    def get_queryset(self):
        base = super(TaskListView, self).get_queryset()
        return base.filter(user=self.request.user)
        
class TaskAddView(LoginRequiredMixin, generic.edit.CreateView, SuccessMessageMixin):
    model = Task
    success_url = reverse_lazy('todo:home')
    success_message = "Task \"%(title)s\" successfully added"
    fields = ['title', 'notes', 'importance', 'duration']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TaskEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model= Task
    success_url = reverse_lazy('todo:home')
    template_name_suffix = '_edit_form'
    fields = ['title', 'notes', 'importance', 'duration']
    
    def get_queryset(self):
        base = super(TaskEditView, self).get_queryset()
        return base.filter(user=self.request.user)

    
class TaskDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Task
    success_url = reverse_lazy('todo:home')
    
    def get_queryset(self):
        base = super(TaskDeleteView, self).get_queryset()
        return base.filter(user=self.request.user)

@login_required
def completeTask(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    try:
        task.done= True
        task.save()
        return redirect('todo:home')
    except (Task.DoesNotExist, KeyError):
        render(request, reverse_lazy('todo:home'), {"message":"Task not found"})
        
class PriorityGraphView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        dateAdded = timezone.now()
        data = dict()
        
        for i in range(1,4):
            for j in (1,5,12):
                ij = str(i)+'(imp), '+str(j)+'(dur)'
                data[ij] = {
                    'dates': [],
                    'priorities': [],
                }
                
                for currDate in range(int(dateAdded.timestamp()), int((dateAdded+datetime.timedelta(weeks=2)).timestamp()), 1800):
                    data[ij]['dates'].append(currDate)
                    data[ij]['priorities'].append(getPriority(i,j,dateAdded, datetime.datetime.fromtimestamp(currDate, timezone.utc)))

        
        return Response(data)