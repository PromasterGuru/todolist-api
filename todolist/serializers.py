from todolist.models import Project, Task
from rest_framework.validators import UniqueTogetherValidator
from todolist.base.serializers import ProjectSerializer, TaskSerializer

class ProjectListSerializer(ProjectSerializer):

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        #Override valdiation messages
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['required'] = field_error_messages['null'] \
                = field_error_messages['blank'] = f'Please fill in the project {field}'
        
    def create(self, validated_data):
        project, created = Project.objects.get_or_create(name = validated_data['name'], description=validated_data['description'])
        if not created:
            return super().update(instance=project, validated_data=validated_data)
        return project
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def validate(self, attrs):
        return super().validate(attrs)
    
class ProjectDetailsSerializer(ProjectSerializer):
    class Meta:
        model = Project
        fields = "__all__"
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class TaskListSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(Task.objects.all(), fields=('project', 'name'), message="Task already exists")
        ]

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        #Override valdiation messages
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['required'] = field_error_messages['null'] \
                = field_error_messages['blank'] = f'Please fill in the task {field}'

    def validate(self, attrs):
        return super().validate(attrs)

class TaskDetailsSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = "__all__"
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
