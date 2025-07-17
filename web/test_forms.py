from django.test import TestCase
from .forms import TodoItemForm
from .models import TodoItem


class TodoItemFormTest(TestCase):
    """
    Test cases for the TodoItemForm.
    """
    
    def test_valid_form(self):
        """Test that a form with valid data is valid."""
        form_data = {'content': 'Test todo item'}
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_content(self):
        """Test that empty content is invalid."""
        form_data = {'content': ''}
        form = TodoItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_whitespace_only_content(self):
        """Test that whitespace-only content is invalid."""
        form_data = {'content': '   \n\t   '}
        form = TodoItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_form_save(self):
        """Test that the form saves correctly."""
        form_data = {'content': 'Test todo item'}
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        todo = form.save()
        self.assertIsInstance(todo, TodoItem)
        self.assertEqual(todo.content, 'Test todo item')
        self.assertFalse(todo.is_done)
        self.assertIsNone(todo.marked_as_done_at)
    
    def test_content_cleaning(self):
        """Test that content is properly cleaned (stripped)."""
        form_data = {'content': '  Test todo item  '}
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'Test todo item')