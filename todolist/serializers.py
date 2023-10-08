from rest_framework import serializers
from todolist.models import Project, Task
from rest_framework.validators import UniqueTogetherValidator

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
    
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
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.save()
        return instance
    
    def validate(self, attrs):
        errors = {}
        if((len(attrs['name']) < 5) | (len(attrs['name']) > 50)): 
            errors['name'] = "Project name must be between 4 and 50 characters"
        if((len(attrs['description']) < 50) | (len(attrs['description']) > 250)): 
            errors['description'] = "Project description must be between 50 and 250 characters"
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs
    
class ProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(Task.objects.all(), fields=('project', 'name'))
        ]

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        #Override valdiation messages
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['required'] = field_error_messages['null'] \
                = field_error_messages['blank'] = f'Please fill in the task {field}'

