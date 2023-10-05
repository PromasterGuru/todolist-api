from collections.abc import Iterable
from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
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
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    due_date_at = models.DateTimeField(default=timezone.now, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    deleted_at = models.DateTimeField(null=True)
  
    class Meta:
        ordering = ["-created_at"]
        db_table_comment = "Available Tasks"

    def __str__(self) -> str:
        return self.name
    