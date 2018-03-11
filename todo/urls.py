from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('home/', views.getHome, name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('task/', views.PriorityTaskView.as_view(), name='task'),
    path('add/', views.TaskAddView.as_view(), name='add'),
    path('edit/<int:pk>/', views.TaskEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete'),
    path('complete/<int:pk>/', views.completeTask, name='complete'),
]