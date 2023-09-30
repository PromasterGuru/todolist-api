from rest_framework import serializers
from todolist.models import Project, Task

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project,
        fields = ('project_id','name','description','created_at')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task,
        fields = ('task_id','project_id','name','description','created_at')
