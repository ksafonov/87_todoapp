from fastapi import FastAPI
from typing import List, Optional, Dict, Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from .models import TodoItem
from .forms import TodoItemForm

app = FastAPI()

@csrf_exempt
def todo_list(request: HttpRequest) -> HttpResponse:
    """
    Display all todo items on the main page and handle new todo creation.
    Shows content, creation date, and completion status for each item.
    Handles both GET (display form) and POST (process form) requests.
    """
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo item created successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TodoItemForm()
    
    todos = TodoItem.objects.all().order_by('-created_at')
    
    # Calculate statistics
    total_count = todos.count()
    completed_count = todos.filter(is_done=True).count()
    pending_count = total_count - completed_count
    
    context = {
        'todos': todos,
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'form': form,
    }
    
    return render(request, 'web/todo_list.html', context)

@csrf_exempt
@require_POST
def mark_todo_done(request: HttpRequest, todo_id: int) -> JsonResponse:
    """
    Mark a todo item as done or undone.
    Handles AJAX requests to toggle completion status.
    """
    try:
        todo = get_object_or_404(TodoItem, id=todo_id)
        
        # Toggle the completion status
        if todo.is_done:
            # Mark as not done
            todo.is_done = False
            todo.marked_as_done_at = None
            action = 'unmarked'
        else:
            # Mark as done
            todo.is_done = True
            todo.marked_as_done_at = timezone.now()
            action = 'marked'
        
        todo.save()
        
        return JsonResponse({
            'success': True,
            'action': action,
            'is_done': todo.is_done,
            'marked_as_done_at': todo.marked_as_done_at.strftime('%b %d, %Y %I:%M %p') if todo.marked_as_done_at else None,
            'message': f'Todo item {action} as {"done" if todo.is_done else "pending"}!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_POST
def delete_todo(request: HttpRequest, todo_id: int) -> JsonResponse:
    """
    Delete a todo item permanently.
    Handles AJAX requests to remove todo items from the database.
    """
    try:
        todo = get_object_or_404(TodoItem, id=todo_id)
        todo_content = todo.content[:50] + "..." if len(todo.content) > 50 else todo.content
        
        todo.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Todo item "{todo_content}" has been deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
