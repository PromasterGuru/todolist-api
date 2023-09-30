# todolist/test_views.py
from rest_framework import viewsets
from todolist.serializers import ProjectSerializer, TaskSerializer
from todolist.models import Project, Task

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        return ""

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request):
        return ""
