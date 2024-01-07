from django.contrib import admin
from .models import Todo,Contact
# Register your models here.

admin.site.site_header = 'Todo App'

class TodoAdmin(admin.ModelAdmin):
  list_display = ['text','completed']
  list_filter = ['completed','text']
  search_fields = ['text']

admin.site.register(Todo,TodoAdmin)
admin.site.register(Contact)