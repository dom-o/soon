from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

# Create your tests here.
class TestAuth(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user1', 'user1PASSWORD')
        User.objects.create_user('user2', 'user2PASSWORD')
        
        
    def testCreateAndEditTasks(self):
        c = self.client
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        c.logout()
        c.force_login(user1)
        
        task = Task(title='User1 Task 1', user=user1)
        task.save()
        
        #When you're logged in accessing data that's yours, everything should work as planned.
        response = c.get(reverse('todo:task'))
        self.assertContains(response, 'User1 Task 1', status_code=200)
        
        response = c.get(reverse('todo:edit', kwargs={'pk':task.pk}))
        self.assertEqual(response.status_code, 200)
        
        response = c.get(reverse('todo:complete', kwargs={'pk':task.pk}))
        task.refresh_from_db()
        self.assertTrue(task.done)
        self.assertRedirects(response, reverse('todo:home'), target_status_code=302)
        
        #Trying to access tasks when you're logged out.
        #Basically should just tell you to log in.
        c.logout()
        
        response = c.get(reverse('todo:task'))
        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('todo:task')))
        
        response = c.get(reverse('todo:edit', kwargs={'pk':task.pk}))
        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('todo:edit', kwargs={'pk':task.pk})))
        
        response = c.get(reverse('todo:delete', kwargs={'pk':task.pk}))
        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('todo:delete', kwargs={'pk':task.pk})))
        
        response = c.get(reverse('todo:complete', kwargs={'pk':task.pk}))
        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('todo:complete', kwargs={'pk':task.pk})))
        
        #This block tests trying to access tasks that aren't yours; should just not find them.
        c.force_login(user2)
        
        response = c.get(reverse('todo:task'))
        self.assertContains(response, 'No tasks', status_code=200)
        
        response = c.get(reverse('todo:edit', kwargs={'pk':task.pk}))
        self.assertEqual(response.status_code, 404)
        
        response = c.get(reverse('todo:delete', kwargs={'pk':task.pk}))
        self.assertEqual(response.status_code, 404)
        
        response = c.get(reverse('todo:complete', kwargs={'pk':task.pk}))
        self.assertEqual(response.status_code, 404)
        
class TestTaskView(TestCase):
    