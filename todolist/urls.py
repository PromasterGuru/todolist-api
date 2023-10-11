# todolist/urls.py
from django.urls import path

from todolist.views import *

urlpatterns = [
    path('projects/', ProjectListCreateApiView.as_view(), name='api-project-list'),
    path('project/<int:project_id>/', ProjectDetailsApiView.as_view(), name='api-project-detail'),
    path('project/<int:project_id>/tasks/', TaskListCreateApiView.as_view(), name='api-project-tasks-list'),
    path('project/<int:project_id>/task/<int:task_id>/', TaskDetailsApiView.as_view(), name='api-task-detail'),
]
