from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.getHome, name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('task/', views.PriorityTaskView.as_view(), name='task'),
    path('add/', views.TaskAddView.as_view(), name='add'),
    path('edit/<int:pk>/', views.TaskEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete'),
    path('complete/<int:pk>/', views.completeTask, name='complete'),
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('task-list/', views.TaskListView.as_view(), name='task-list'),
    path('api/task/priority', views.PriorityGraphView.as_view(), name='api-priority-data'),
    path('analytics/priority', TemplateView.as_view(template_name='analytics/task_priority.html')),
]