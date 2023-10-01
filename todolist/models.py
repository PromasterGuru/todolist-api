from django.db import models
import uuid
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ["-created_at"]
        db_table_comment = "Available Projects"


class Task(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    due_date_at = models.DateTimeField(auto_now=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_task_id(self):
        return str(uuid.uuid4()).split("-")[-1]
    
    def save(self, *args, **kwargs):
        project = Project.objects.get(name=self.project.name)
        if(project is None):
            return f"Project for this task {self.name} not found"
        super(Task, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ["-created_at"]
        db_table_comment = "Available Tasks"