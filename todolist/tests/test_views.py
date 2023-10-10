import json
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status
from todolist.models import Project, Task

"""
---------------------------------------------------------------------
                        PROJECT UNIT TESTS
--------------------------------------------------------------------
"""
class ProjectListCreateApiViewTest(APITestCase):

    def setUp(self) -> None:
        self.data = { 'name': 'Hackathon', 'description': 'In your application code (e.g., in your backend server)' }
        self.url = reverse('api-project-list', kwargs= {'version': 'v1'})

    def test_should_create_a_new_project(self):
        self.assertEquals(Project.objects.count(), 0)
        response = self.client.post(path=self.url, data=self.data, format='json')
        data = response.json()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(data['data']['message'], 'Project created successfully')
        self.assertEquals(Project.objects.count(), 1)
    
    def test_should_update_existing_project_when_duplicate_project_is_created(self):
        project1 = Project.objects.create(name=self.data['name'], description=self.data['description'])
        response = self.client.post(path=self.url, data=self.data, format='json')
        data = response.json()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(project1.pk, data['data']['details']['id'])
        self.assertEquals(Project.objects.count(), 1)
    
    def test_should_throw_exception_when_project_name_has_invalid_length(self):
        sample = self.data
        sample['name'] = "Test"
        response = self.client.post(path=self.url, data=self.data, format='json')
        data = response.json()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(data['data']['details']['error_code'], 'SERVER_VALIDATION_FAILURE')
    
    def test_should_throw_exception_when_project_description_has_invalid_length(self):
        sample = self.data
        sample['description'] = "Test Description"
        response = self.client.post(path=self.url, data=self.data, format='json')
        data = response.json()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(data['data']['details']['error_code'], 'SERVER_VALIDATION_FAILURE')

    def test_should_throw_exception_when_retrieving_projects_from_empty_db(self):
        response = self.client.get(path=self.url)
        data = response.json()
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(data['data']['details']['error_code'], 'PROJECT_RECORD_NOT_FOUND')

    def test_should_get_projects(self):
        Project.objects.create(name=self.data['name'], description=self.data['description'])
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data['data']['message'], 'Projects record retrieved successfully')
        self.assertGreater(len(data['data']['details']), 0)
 
class ProjectDetailsCreateApiViewTest(APITestCase):

    def setUp(self) -> None:
        self.data = { 'name': 'Hackathon', 'description': 'In your application code (e.g., in your backend server)' }
        self.project = Project.objects.create(name=self.data['name'], description=self.data['description'])
        self.url = reverse('api-project-detail', kwargs={'version': 'v1', 'pk': self.project.pk})
        self.unexisting_project_url = reverse('api-project-detail', kwargs={'version': 'v1', 'pk':0})
    
    def test_should_get_project_by_project_id(self):
        response = self.client.get(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data['data']['details']['id'], self.project.pk)
        
    def test_should_throw_project_not_found_exception_when_retrieving_unexisting_project(self):
        response = self.client.get(path=self.unexisting_project_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_update_project_if_exists(self):
        sample = self.data
        sample['name'] = "New Record"
        response = self.client.put(path=self.url, data=sample, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEquals(self.project.name, sample['name'])
        self.assertEquals(self.project.description, sample['description'])
    
    def test_update_should_create_a_new_project_if_does_not_exists(self):
        sample = self.data
        sample['name'] = "New Record"
        response = self.client.put(path=self.unexisting_project_url, data=sample, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEquals(Project.objects.count(), 2)
        self.assertEquals(data['data']['details']['name'], sample['name'])
        self.assertEquals(data['data']['details']['description'], sample['description'])

    def test_should_delete_existing_project(self):
        self.assertEquals(Project.objects.count(), 1)
        response = self.client.delete(path=self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Project.objects.count(), 0)
    
    def test_should_throw_exception_when_deleting_unexisting_project(self):
        self.assertEquals(Project.objects.count(), 1)
        response = self.client.delete(path=self.unexisting_project_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


# """
# ---------------------------------------------------------------------
#                         TASKS UNIT TESTS
# ---------------------------------------------------------------------
# """
# class ProjectTaskListCreateApiViewTest(APITestCase):

#     def setUp(self) -> None:
#         self.project = Project.objects.create(name='Creative Todo', description='Task management project')
#         self.url = reverse('api-project-tasks-list', kwargs= {'version': 'v1', 'pk': self.project.pk})
#         self.data = {'name': 'UI/UX Design', 'description': 'Design figma designs'}

#     def test_create_task(self):
#             self.assertEquals(Project.objects.count(), 1)
#             self.assertEquals(Task.objects.count(), 0)
#             response = self.client.post(path=self.url, data=self.data, format='json')
#             self.assertEquals(response.status_code, status.HTTP_201_CREATED)
#             task = Task.objects.first()
#             self.assertEquals(task.name, self.data['name'])

#     def test_get_tasks_when_there_are_no_tasks_on_db(self):
#         response = self.client.get(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         self.assertEquals(len(response.json()), 0)

#     def test_get_tasks(self):
#         Task.objects.create(name=self.data['name'], description=self.data['description'])
#         response = self.client.get(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEquals(data[0]['name'], self.data['name'])
#         self.assertEquals(data[0]['description'], self.data['description'])

# class TaskDetailsCreateApiViewTest(APITestCase):

#     def setUp(self) -> None:
#         self.data = {'name':'Database Design', 'description':'Create class and ERD Diagrams'}
#         self.project = Project.objects.create(name='Creative Todo', description='Task management project')
#         self.task = Task.objects.create(name="Load Testing", description="Perform load tests", project=self.project)
#         self.url = reverse('api-task-detail', kwargs={'version': 'v1', 'pk': self.task.pk})
#         self.invalid_url = reverse('api-task-detail', kwargs={'version': 'v1', 'pk': -999})
    
#     def test_get_task(self):
#         response = self.client.get(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEquals(data['id'], self.task.pk)
#         self.assertEquals(data['name'], self.task.name)
#         self.assertEquals(data['description'], self.task.description)

#     def test_update_task(self):
#         response = self.client.get(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         data = {
#             'name': "Architecture",
#             'description': "Database Architecture"
#         }
#         response = self.client.put(path=self.url, data=data, format='json')
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         self.task.refresh_from_db()
#         self.assertEquals(self.task.name, data['name'])
#         self.assertEquals(self.task.description, data['description'])

#     def test_update_unexisting_task(self):
#         data = {
#             'name': "Hobby",
#             'description': "Playing Guitar"
#         }
#         response = self.client.put(path=self.invalid_url, data=data, format='json')
#         self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
    
#     def test_delete_task(self):
#         self.assertEquals(Task.objects.count(), 1)
#         response = self.client.delete(path=self.url)
#         self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEquals(Task.objects.count(), 0)
    
#     def test_delete_unexisting_task(self):
#         self.assertEquals(Task.objects.count(), 1)
#         response = self.client.delete(path=self.invalid_url)
#         self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEquals(Task.objects.count(), 1)
        
