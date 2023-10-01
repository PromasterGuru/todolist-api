from rest_framework import serializers
from todolist.models import Project, Task

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('pk','name','description','created_at', 'updated_at')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('pk','project','name','description','created_at', 'updated_at')
