# todolist/urls.py
from django.urls import path

from todolist.views import *

urlpatterns = [
    path('projects/', ProjectListCreateApiView.as_view(), name='api-project-list'),
    path('project/<int:pk>/', ProjectDetailsApiView.as_view(), name='api-project-detail'),
    path('tasks/<int:pk>/', TaskListCreateApiView.as_view(), name='api-project-tasks-list'),
    path('task/<int:pk>/', TaskDetailsApiView.as_view(), name='api-task-detail'),
]
