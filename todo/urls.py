from django.urls import path
from . import views

urlpatterns = [
    path('',views.lists,name='todo'),
    path('create',views.create,name='create'),
    path('edit/<int:pk>',views.edit_todo,name='edit-todo'),
    path('delete/<int:pk>',views.delete_todo,name='delete-todo'),
    path('status/<int:pk>',views.status_todo,name='todo-status'),

    path('contact',views.contact,name='contact'),
    path('create-contact',views.create_contact,name='create-contact'),
    path('delete-contact/<int:pk>',views.delete_contact,name='delete-contact'),

    path('search',views.search_view,name='search'),
    path('search-result',views.search_results_view,name='search-result'),

]
