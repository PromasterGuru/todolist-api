# todolist/urls.py
from django.urls import path

from todolist.views import ProjectListCreateApiView, ProjectDetailCreateApiView, TaskListCreateApiView, TaskDetailCreateApiView

urlpatterns = [
    path('projects/', ProjectListCreateApiView.as_view(), name='api-project-list'),
    path('projects/<pk>/', ProjectDetailCreateApiView.as_view(), name='api-project-detail'),
    path('tasks/', TaskListCreateApiView.as_view(), name='api-task-list'),
    path('tasks/<pk>/', TaskDetailCreateApiView.as_view(), name='api-task-detail'),
]
