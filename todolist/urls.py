# todolist/urls.py
from django.urls import path

from todolist.views import *

urlpatterns = [
    path('projects/', ProjectListCreateApiView.as_view(), name='api-project-list'),
    path('project/<pk>', ProjectDetailCreateApiView.as_view(), name='api-project-detail'),
    path('tasks/<pk>', ProjectTaskListCreateApiView.as_view(), name='api-project-tasks-list'),
    path('task/<pk>', TaskDetailCreateApiView.as_view(), name='api-task-detail'),
]
