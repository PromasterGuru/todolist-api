# todolist/urls.py
from django.urls import include, path

from .views import ProjectViewSet, TaskViewSet

urlpatterns = [
    path('', ProjectViewSet.as_view, name='project'),
    path('task/<task>', TaskViewSet.as_view, name='task')
]
