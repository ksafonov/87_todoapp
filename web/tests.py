from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import TodoItem
from .forms import TodoItemForm


class TodoListViewTest(TestCase):
    """
    Test cases for the todo_list view.
    """
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo_list')
    
    def test_get_request(self):
        """Test GET request displays the form and todos."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Todo')
        self.assertIsInstance(response.context['form'], TodoItemForm)
    
    def test_post_valid_form(self):
        """Test POST request with valid form data creates todo."""
        form_data = {'content': 'Test todo item'}
        response = self.client.post(self.url, data=form_data)
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        
        # Todo should be created
        self.assertEqual(TodoItem.objects.count(), 1)
        todo = TodoItem.objects.first()
        self.assertEqual(todo.content, 'Test todo item')
        self.assertFalse(todo.is_done)
    
    def test_post_invalid_form(self):
        """Test POST request with invalid form data shows errors."""
        form_data = {'content': ''}
        response = self.client.post(self.url, data=form_data)
        
        # Should not redirect, should show form with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below')
        
        # No todo should be created
        self.assertEqual(TodoItem.objects.count(), 0)
    
    def test_success_message(self):
        """Test that success message is displayed after creating todo."""
        form_data = {'content': 'Test todo item'}
        response = self.client.post(self.url, data=form_data, follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Todo item created successfully!')
    
    def test_empty_state_display(self):
        """Test that empty state is displayed when no todos exist."""
        response = self.client.get(self.url)
        self.assertContains(response, 'No todos yet')
        self.assertContains(response, 'Use the form above to add your first todo item')
    
    def test_todos_display(self):
        """Test that existing todos are displayed correctly."""
        # Create a test todo
        todo = TodoItem.objects.create(content='Test todo item')
        
        response = self.client.get(self.url)
        self.assertContains(response, 'Test todo item')
        self.assertContains(response, 'Total Tasks')
        self.assertEqual(response.context['total_count'], 1)
        self.assertEqual(response.context['pending_count'], 1)
        self.assertEqual(response.context['completed_count'], 0)
