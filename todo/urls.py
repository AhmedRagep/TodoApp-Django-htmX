from django.urls import path
from . import views

urlpatterns = [
    path('',views.lists,name='todo'),
    path('create',views.create,name='create'),
    path('edit/<int:pk>',views.edit_todo,name='edit-todo'),
    path('delete/<int:pk>',views.delete_todo,name='delete-todo'),
    path('status/<int:pk>',views.status_todo,name='todo-status'),
]
