# todolist/test_views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from todolist.serializers import ProjectSerializer, TaskSerializer
from todolist.models import Project, Task

class ProjectListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of projects or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

class ProjectDetailCreateApiView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete project
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

class ProjectTaskListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of project tasks or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskSerializer

class TaskListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of tasks or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class TaskDetailCreateApiView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete task
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
