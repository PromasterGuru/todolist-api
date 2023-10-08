# todolist/test_views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from todolist.serializers import ProjectListSerializer, TaskSerializer, ProjectDetailsSerializer
from todolist.models import Project, Task
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK

class ProjectListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of projects or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ProjectListSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        if len(serializer.errors) > 0:
            return Response(data={'data': {
                'message': 'Invalid inputs',
                'details': {
                    'server_error': serializer.errors,
                    'error_code': 'INPUT_VALIDATION_FAILURE'
                }} 
            }, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={"data": {"message": "Project created successfully", "details": serializer.data}},status=HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        try:
            projects = Project.objects.all()
            breakpoint()
            if(len(projects) > 0):
                serializer = ProjectListSerializer(projects)
                serializer.is_valid(raise_exception=True)
                return Response(data={"data": {"message": "Projects record retrieved successfully", "details": serializer.data}},status=HTTP_200_OK)
            raise Project.DoesNotExist('No project records found') 
        except Project.DoesNotExist as e:
            return Response(data={'data': {
                'message': 'No projects records found', 
                'details': {
                    'server_error': e.args[0],
                    'error_code': 'PROJECT_RECORD_NOT_FOUND'
                }}
            }, status=HTTP_404_NOT_FOUND)

    
class ProjectDetailCreateApiView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete project
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectDetailsSerializer
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            Project.objects.get(id=kwargs['pk'])
            return super().get(request, *args, **kwargs)
        except Project.DoesNotExist as e:
            return Response(data={'data': {
                'message': 'Project does not exist', 
                'details': {
                    'server_error': e.args[0],
                    'error_code': 'PROJECT_DOES_NOT_EXIST'
                }}
            }, status=HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
           project, created = Project.objects.get_or_create(id=kwargs['pk'])
           if not created:
               return super().update(request, *args, **kwargs)
           return project

class ProjectTaskListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of project tasks or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        """Override post method to validate project before creating task"""
        try:
            project = Project.objects.get(id=kwargs['pk'])
            request.data['project'] = project
            return super().create(request, *args, **kwargs)
        except Project.DoesNotExist as e:
            return Response(data={'data': {
                'message': 'Project does not exist', 
                'details': {
                    'server_error': e.args[0],
                    'error_code': 'PROJECT_DOES_NOT_EXIST'
                }}
            }, status=HTTP_404_NOT_FOUND)

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
