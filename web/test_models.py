from django.test import TestCase
from django.utils import timezone
from web.models import TodoItem


class TodoItemModelTest(TestCase):
    """Test cases for the TodoItem model."""

    def setUp(self):
        """Set up test data."""
        # Create a basic todo item
        self.todo_item = TodoItem.objects.create(
            content="Test todo item"
        )
        
        # Create a completed todo item
        self.completed_todo = TodoItem.objects.create(
            content="Completed todo item",
            is_done=True,
            marked_as_done_at=timezone.now()
        )

    def test_todo_item_creation(self):
        """Test that a TodoItem can be created."""
        self.assertEqual(self.todo_item.content, "Test todo item")
        self.assertFalse(self.todo_item.is_done)
        self.assertIsNone(self.todo_item.marked_as_done_at)
        self.assertIsNotNone(self.todo_item.created_at)
        
        # Check that the created_at field is populated with the current time
        self.assertLessEqual(
            (timezone.now() - self.todo_item.created_at).total_seconds(), 
            10  # Allow for a small time difference
        )

    def test_todo_item_string_representation(self):
        """Test the string representation of a TodoItem."""
        self.assertEqual(str(self.todo_item), str(self.todo_item.id))
        
        # Note: This test might fail if you have a custom __str__ method.
        # If so, update this test to match your expected string representation.

    def test_completed_todo_item(self):
        """Test a completed TodoItem."""
        self.assertEqual(self.completed_todo.content, "Completed todo item")
        self.assertTrue(self.completed_todo.is_done)
        self.assertIsNotNone(self.completed_todo.marked_as_done_at)
        
        # Check that the marked_as_done_at field is populated with the current time
        self.assertLessEqual(
            (timezone.now() - self.completed_todo.marked_as_done_at).total_seconds(), 
            10  # Allow for a small time difference
        )

    def test_mark_todo_as_done(self):
        """Test marking a TodoItem as done."""
        # Initially the todo item is not done
        self.assertFalse(self.todo_item.is_done)
        self.assertIsNone(self.todo_item.marked_as_done_at)
        
        # Mark it as done
        self.todo_item.is_done = True
        self.todo_item.marked_as_done_at = timezone.now()
        self.todo_item.save()
        
        # Refresh from database
        self.todo_item.refresh_from_db()
        
        # Check that it's now marked as done
        self.assertTrue(self.todo_item.is_done)
        self.assertIsNotNone(self.todo_item.marked_as_done_at)

    def test_todo_item_update(self):
        """Test updating a TodoItem."""
        # Update the content
        self.todo_item.content = "Updated content"
        self.todo_item.save()
        
        # Refresh from database
        self.todo_item.refresh_from_db()
        
        # Check that the content was updated
        self.assertEqual(self.todo_item.content, "Updated content")

    def test_todo_item_deletion(self):
        """Test deleting a TodoItem."""
        # Get the initial count
        initial_count = TodoItem.objects.count()
        
        # Delete a todo item
        self.todo_item.delete()
        
        # Check that the count decreased by 1
        self.assertEqual(TodoItem.objects.count(), initial_count - 1)
        
        # Check that the specific todo item is gone
        with self.assertRaises(TodoItem.DoesNotExist):
            TodoItem.objects.get(id=self.todo_item.id)

    def test_filter_done_items(self):
        """Test filtering for done TodoItems."""
        # Get all done items
        done_items = TodoItem.objects.filter(is_done=True)
        
        # Check that our completed todo is in the list
        self.assertIn(self.completed_todo, done_items)
        
        # Check that our incomplete todo is not in the list
        self.assertNotIn(self.todo_item, done_items)
        
        # Check the count
        self.assertEqual(done_items.count(), 1)

    def test_filter_undone_items(self):
        """Test filtering for undone TodoItems."""
        # Get all undone items
        undone_items = TodoItem.objects.filter(is_done=False)
        
        # Check that our incomplete todo is in the list
        self.assertIn(self.todo_item, undone_items)
        
        # Check that our completed todo is not in the list
        self.assertNotIn(self.completed_todo, undone_items)
        
        # Check the count
        self.assertEqual(undone_items.count(), 1)

    def test_bulk_creation(self):
        """Test creating multiple TodoItems at once."""
        # Get the initial count
        initial_count = TodoItem.objects.count()
        
        # Create multiple todo items
        new_todos = [
            TodoItem(content="Bulk todo 1"),
            TodoItem(content="Bulk todo 2"),
            TodoItem(content="Bulk todo 3"),
        ]
        TodoItem.objects.bulk_create(new_todos)
        
        # Check that the count increased by 3
        self.assertEqual(TodoItem.objects.count(), initial_count + 3)
        
        # Check that the items were created with the correct content
        self.assertTrue(TodoItem.objects.filter(content="Bulk todo 1").exists())
        self.assertTrue(TodoItem.objects.filter(content="Bulk todo 2").exists())
        self.assertTrue(TodoItem.objects.filter(content="Bulk todo 3").exists())