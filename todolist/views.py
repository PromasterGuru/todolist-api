# todolist/test_views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from todolist.serializers import ProjectListSerializer, TaskSerializer, ProjectDetailsSerializer
from todolist.models import Project, Task
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from todolist.validators.validators import ProjectValidator

class ProjectListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of projects or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    validator = ProjectValidator()

    def create(self, request, *args, **kwargs):
        serializer = ProjectListSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        if len(serializer.errors) > 0:
            return self.validator.server_validation_exception(errors=serializer.errors)
        serializer.save()
        return Response(data={'data': {'message': 'Project created successfully', 'details': serializer.data}},status=HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        try:
            projects_queryset = Project.objects.all()
            serializer = ProjectListSerializer(projects_queryset, many=True)
            if(len(serializer.data) > 0):
                return Response(data={'data': {'message': 'Projects record retrieved successfully', 'details': serializer.data}},status=HTTP_200_OK)
            raise Project.DoesNotExist("You have no projects at the moment, create a new one to start.")
        except Project.DoesNotExist as e:
            return self.validator.server_exception(title='No projects records found',errors=e.args[0], code='PROJECT_RECORD_NOT_FOUND', status_code=HTTP_404_NOT_FOUND)

class ProjectDetailCreateApiView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete project
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectDetailsSerializer
    queryset = Project.objects.all()
    validator = ProjectValidator()

    def get(self, _, **kwargs):
        try:
            project_queryset = Project.objects.get(id=kwargs['pk'])
            serializer = ProjectDetailsSerializer(project_queryset)
            return Response(data={'data': {'message': 'Project record retrieved successfully', 'details': serializer.data}},status=HTTP_200_OK)
        except Project.DoesNotExist as e:
            return self.validator.server_exception(title='Project does not exist', errors=e.args[0], code='PROJECT_DOES_NOT_EXIST',status_code=HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
            try:
                serializer = ProjectDetailsSerializer(data=request.data, many=False)
                serializer.is_valid(raise_exception=False)
                if len(serializer.errors) > 0:
                    return self.validator.server_exception(serializer.errors, 'PROJECT_UPDATE_FAILURE')
                updated_values = {'name':request.data['name'], 'description':request.data['description']}
                project, created = Project.objects.update_or_create(id=kwargs['pk'], defaults=updated_values)
                status_code = HTTP_201_CREATED if created else HTTP_200_OK
                serializer = ProjectDetailsSerializer(project)
                return Response(data={'data': {'message': 'Project record updated successfully', 'details': serializer.data}},status=status_code)
            except BaseException as e:
                return self.validator.server_exception(title='Failed to update project', errors=e.args[0], code='PROJECT_RECORD_NOT_UPDATED')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Project.DoesNotExist as e:
            return self.validator.server_exception(title='Project does not exist', errors=e.args[0], code='PROJECT_DOES_NOT_EXIST', status_code=HTTP_404_NOT_FOUND)

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
            return self.server_exception(title='Project does not exist', errors=e.args[0], code='PROJECT_DOES_NOT_EXIST')

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
