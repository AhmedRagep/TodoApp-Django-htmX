from django.shortcuts import redirect, render
from .models import Todo
from django.http import HttpResponse
# Create your views here.

# def todo(request):
#   if request.POST:
#     text = request.POST['name']
#     create = Todo.objects.create(text=text)
#     create.save()
#     return redirect('todo')
#   else:
#     print('hello')
#   todo_all = Todo.objects.all().order_by('-id')[:5]
#   context = {
#     'todo_all':todo_all
#   }
#   return render(request,'todo.html',context)

def lists(request):
  todo_all = Todo.objects.all().order_by('-id')[:7]
  return render(request,"todo.html",{'todo_all':todo_all})


def create(request):
  if request.POST.get('todo_id'):
    todo_id = request.POST.get('todo_id')
    todo_text = Todo.objects.get(id=todo_id)
    todo_text.text = request.POST.get('name')
    todo_text.save()
  else:
    text_name = request.POST.get('name')
    text = Todo.objects.create(text=text_name)

  todo_all = Todo.objects.all().order_by('-id')[:7]
  context = {
    'todo_all':todo_all
  }
  return render(request,"todo.html",context)


def edit_todo(request,pk):
  todo = Todo.objects.get(id=pk)
  return HttpResponse(f'''
                      <input type="hidden" value="{todo.id}" name="todo_id" id="">
                      <input class="form-control" style="height: 50px;" type="text" value="{todo.text}" placeholder="Enter ToDo" name="name" id="input">
                      
                      ''')


def delete_todo(request,pk):
  todo_text = Todo.objects.get(id=pk)
  todo_text.delete()
  todo_all = Todo.objects.all().order_by('-id')[:7]
  context = {
    'todo_all':todo_all
  }
  return render(request,"todo.html",context)

  