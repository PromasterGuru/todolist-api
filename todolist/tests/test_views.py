import json
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status
from todolist.models import Project, Task

"""
Projects tests: CRUD
"""
class ProjectListCreateApiViewTest(APITestCase):

    def setUp(self) -> None:
        self.data = { 'name': 'Hackathon', 'description': 'We base payment method' }
        self.url = reverse('api-project-list', kwargs= {'version': 'v1'})

    def test_create_project(self):
        self.assertEquals(Project.objects.count(), 0)
        response = self.client.post(path=self.url, data=self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.first()
        self.assertEquals(project.name, self.data['name'])
        self.assertEquals(project.description, self.data['description'])

    def test_get_projects_when_there_are_no_projects_on_db(self):
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), 0)

    def test_get_projects(self):
        Project.objects.create(name=self.data['name'], description=self.data['description'])
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data[0]['name'], self.data['name'])
        self.assertEquals(data[0]['description'], self.data['description'])
 
class ProjectDetailsCreateApiViewTest(APITestCase):

    def setUp(self) -> None:
        self.project = Project.objects.create(name="Leisure", description="Listen to music")
        self.url = reverse('api-project-detail', kwargs={'version': 'v1', 'pk': self.project.pk})
        self.invalid_url = reverse('api-project-detail', kwargs={'version': 'v1', 'pk': -999})
    
    def test_get_project(self):
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data['id'], self.project.pk)
        self.assertEquals(data['name'], self.project.name)
        self.assertEquals(data['description'], self.project.description)
        
    def test_get_unexisting_project(self):
        response = self.client.get(path=self.invalid_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project(self):
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = {
            'name': "Hobby",
            'description': "Playing Guitar"
        }
        response = self.client.put(path=self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEquals(self.project.name, data['name'])
        self.assertEquals(self.project.description, data['description'])
    
    def test_update_unexisting_project(self):
        data = {
            'name': "Hobby",
            'description': "Playing Guitar"
        }
        response = self.client.put(path=self.invalid_url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_project(self):
        self.assertEquals(Project.objects.count(), 1)
        response = self.client.delete(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Project.objects.count(), 0)
    
    def test_delete_unexisting_project(self):
        self.assertEquals(Project.objects.count(), 1)
        response = self.client.delete(path=self.invalid_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

"""
Tasks tests: CRUD
"""
class ProjectTaskListCreateApiViewTest(APITestCase):

    def setUp(self) -> None:
        self.project = Project.objects.create(name='Creative Todo', description='Task management project')
        self.url = reverse('api-project-tasks-list', kwargs= {'version': 'v1', 'pk': self.project.pk})

    def test_create_task(self):
        self.assertEquals(Project.objects.count(), 1)
        self.assertEquals(Task.objects.count(), 0)
        data = {
            'name': 'UI/UX Design',
            'description': 'Design figma designs',
        }
        response = self.client.post(path=self.url, data=data, format='json')
        tasks = Task.objects.all()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(tasks.count(), 1)
        self.assertEquals(tasks[0].name, data['name'])
        self.assertEquals(tasks[0].description, data['description'])

class TaskListCreateApiViewTest(APITestCase):

    def setUp(self) -> None:
        self.data = {'name': 'UI/UX Design', 'description': 'Design figma designs'}
        self.project = Project.objects.create(name='Creative Todo', description='Task management project')
        self.url = reverse('api-project-tasks-list', kwargs= {'version': 'v1', 'pk': self.project.pk})

    def test_create_task(self):
        self.assertEquals(Project.objects.count(), 1)
        self.assertEquals(Task.objects.count(), 0)
        response = self.client.post(path=self.url, data=self.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.first()
        self.assertEquals(task.name, self.data['name'])

    def test_get_tasks(self):
        Task.objects.create(name=self.data['name'], description=self.data['description'])
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data[0]['name'], self.data['name'])
        self.assertEquals(data[0]['description'], self.data['description'])

# class TaskDetailsCreateApiViewTest(APITestCase):

#     def setUp(self) -> None:
#         self.project = Project.objects.create(name='Creative Todo', description='Task management project')
#         self.task = Task.objects.create(name='Database Design', description='Create class and ERD Diagrams', project=self.project)
#         self.url = reverse('api-task-detail', kwargs={'version': 'v1', 'pk': self.task.pk})
    
#     def test_get_task(self):
#         response = self.client.get(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEquals(data['pk'], str(self.task.pk))
#         self.assertEquals(data['name'], self.task.name)
#         self.assertEquals(data['description'], self.task.description)

#     def test_update_task(self):
#         response = self.client.get(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         data = {
#             'pk': self.task.pk,
#             'name': "Architecture",
#             'description': "Database Architecture"
#         }
#         response = self.client.put(path=self.url, data=data, format='json')
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         self.task.refresh_from_db()
#         self.assertEquals(self.task.name, data['name'])
#         self.assertEquals(self.task.description, data['description'])

#     def test_delete_task(self):
#         self.assertEquals(Task.objects.count(), 1)
#         response = self.client.delete(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEquals(Task.objects.count(), 0)
