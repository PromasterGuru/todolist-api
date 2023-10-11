# todolist/test_views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from todolist.serializers import ProjectListSerializer, TaskListSerializer, ProjectDetailsSerializer, TaskDetailsSerializer
from todolist.models import Project, Task
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK
from todolist.validators.validators import AppValidator

class ProjectListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of projects or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    validator = AppValidator()

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

class ProjectDetailsApiView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete project
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProjectDetailsSerializer
    queryset = Project.objects.all()
    validator = AppValidator()

    def get(self, request, *args, **kwargs):
        try:
            project_queryset = Project.objects.get(id=kwargs['project_id'])
            serializer = ProjectDetailsSerializer(project_queryset)
            return Response(data={'data': {'message': 'Project record retrieved successfully', 'details': serializer.data}},status=HTTP_200_OK)
        except Project.DoesNotExist as e:
            return self.validator.server_exception(title='Project does not exist', errors=e.args[0], code='PROJECT_DOES_NOT_EXIST',status_code=HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
            try:
                serializer = ProjectDetailsSerializer(data=request.data, many=False)
                serializer.is_valid(raise_exception=False)
                if len(serializer.errors) > 0:
                    return self.validator.server_validation_exception(serializer.errors, 'PROJECT_UPDATE_FAILURE')
                updated_values = {'name':request.data['name'], 'description':request.data['description']}
                project, created = Project.objects.update_or_create(id=kwargs['project_id'], defaults=updated_values)
                status_code = HTTP_201_CREATED if created else HTTP_200_OK
                serializer = ProjectDetailsSerializer(project)
                return Response(data={'data': {'message': 'Project record updated successfully', 'details': serializer.data}},status=status_code)
            except BaseException as e:
                return self.validator.server_exception(title='Failed to update project', errors=e.args[0], code='PROJECT_RECORD_NOT_UPDATED')

    def delete(self, request, *args, **kwargs):
        try:
            project_queryset = Project.objects.get(pk=kwargs['project_id'])
            project_queryset.delete()
            return Response(data={'data': {'message': 'Project deleted successfully', 'details': {}}},status=HTTP_200_OK)
        except Project.DoesNotExist as e:
            return self.validator.server_exception(title='Project does not exist', errors=e.args[0], code='PROJECT_DOES_NOT_EXIST', status_code=HTTP_404_NOT_FOUND)

class TaskListCreateApiView(ListCreateAPIView):
    """
    API view to retrieve list of project tasks or create new
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    validator = AppValidator()

    def create(self, request, *args, **kwargs):
        """Override post method to validate project before creating task"""
        request.data['project'] = kwargs['project_id']
        serializer = TaskListSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        if len(serializer.errors) > 0:
            return self.validator.server_validation_exception(errors=serializer.errors)
        serializer.save()
        return Response(data={'data': {'message': 'Task created successfully', 'details': serializer.data}},status=HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        try:
            tasks_queryset = Task.objects.filter(project=kwargs['project_id'])
            serializer = TaskListSerializer(tasks_queryset, many=True)
            if(len(serializer.data) > 0):
                return Response(data={'data': {'message': 'Tasks record retrieved successfully', 'details': serializer.data}},status=HTTP_200_OK)
            raise Task.DoesNotExist("You have no tasks at the moment, create a new one to start.")
        except Task.DoesNotExist as e:
            return self.validator.server_exception(title='No tasks records found',errors=e.args[0], code='TASKS_RECORD_NOT_FOUND', status_code=HTTP_404_NOT_FOUND)

class TaskDetailsApiView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete task
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = TaskDetailsSerializer
    queryset = Task.objects.all()
    validator = AppValidator()

    def get(self, request, *args, **kwargs):
        try:
            task_queryset = Task.objects.get(project=kwargs['project_id'], id=kwargs['task_id'])
            serializer = TaskDetailsSerializer(task_queryset)
            return Response(data={'data': {'message': 'Task record retrieved successfully', 'details': serializer.data}},status=HTTP_200_OK)
        except Task.DoesNotExist as e:
            return self.validator.server_exception(title='Task does not exist', errors=e.args[0], code='TASK_DOES_NOT_EXIST',status_code=HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
        try:
            request.data['project'] = kwargs['project_id']
            serializer = TaskDetailsSerializer(data=request.data, many=False)
            serializer.is_valid(raise_exception=False)
            if len(serializer.errors) > 0:
                return self.validator.server_validation_exception(serializer.errors)
            updated_values = {'name':request.data['name'], 'description':request.data['description'], 'project': Project.objects.get(id=kwargs['project_id'])}
            task, created = Task.objects.update_or_create(id=kwargs['task_id'], defaults=updated_values)
            status_code = HTTP_201_CREATED if created else HTTP_200_OK
            serializer = TaskDetailsSerializer(task)
            return Response(data={'data': {'message': 'Task record updated successfully', 'details': serializer.data}},status=status_code)
        except BaseException as e:
            return self.validator.server_exception(title='Failed to update task', errors=e.args[0], code='TASK_RECORD_NOT_UPDATED')