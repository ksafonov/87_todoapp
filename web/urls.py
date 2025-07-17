from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/mark-done/', views.mark_todo_done, name='mark_todo_done'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
]