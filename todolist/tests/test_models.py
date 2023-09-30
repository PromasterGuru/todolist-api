from django.test import TestCase
from todolist.models import Project, Task


class ProjectTestCase(TestCase):
    def test_post(self):
        self.assertEquals(Project.objects.count(), 0)
        Project.objects.create(name="Code", description="Crack that shit")
        Project.objects.create(name="Test", description="Test that shit")
        Project.objects.create(name="Deploy", description="Deploy that shit")
        self.assertEquals(Project.objects.count(), 3)


class TaskTestCase(TestCase):
    def test_post(self):
        self.assertEquals(Task.objects.count(), 0)
        pobj = Project.objects.create(name="Authentication", description="SSO Task")
        Task.objects.create(project=pobj, name="Write", description="Write code")
        Task.objects.create(project=pobj, name="Edit", description="Debug code")
        self.assertEquals(Task.objects.filter(project=pobj).count(), 2)
        self.assertEquals(Task.objects.filter(project=-9).count(), 0)
