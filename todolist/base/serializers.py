from rest_framework import serializers
from todolist.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def validate(self, attrs):
        errors = {}
        if('name' in attrs and ((len(attrs['name']) < 5) | (len(attrs['name']) > 50))): 
            errors['name'] = "Project name must be between 4 and 50 characters"
        if('description' in attrs and ((len(attrs['description']) < 50) | (len(attrs['description']) > 250))): 
            errors['description'] = "Project description must be between 50 and 250 characters"
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs
    
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.save()
        return instance