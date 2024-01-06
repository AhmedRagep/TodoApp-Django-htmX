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
  # لو فيه حاجه رجعت في المتغير ده وهو خاص بالتعديل فقط
  if request.POST.get('todo_id'):
    # هتجيب الايدي اللي رجع فيه
    todo_id = request.POST.get('todo_id')
    # هتجيب التاسك اللي صاحبة الايدي
    todo_text = Todo.objects.get(id=todo_id)
    # هتعدلها باللي مكتوب في المدخل
    todo_text.text = request.POST.get('name')
    # وهتحفظ
    todo_text.save()
  
  # لو مفيش بيانات في ايدي التعديل يبقي انشاء
  else:
    # هتجيب اللي مكتوب في المدخل
    text_name = request.POST.get('name')
    # وهتنشئ بيه تاسك جديد
    text = Todo.objects.create(text=text_name)
  
  # هتجيب كل التسكات ثاني وهيا دي اللي بتتمرر
  todo_all = Todo.objects.all().order_by('-id')[:7]
  context = {
    'todo_all':todo_all
  }
  return render(request,"todo.html",context)


def edit_todo(request,pk):
  # htmx هتجيب التاسك صاحب الايدي وانا كتبته في 
  todo = Todo.objects.get(id=pk)
  # وهتغير المدخل بمدخل يحتوي علي التاسك اللي ضغط عليها
  # وكمان هضيف الزر المخفي ده اللي بيحتوي علي الايدي
  return HttpResponse(f'''
                      <input type="hidden" value="{todo.id}" name="todo_id" id="">
                      <input class="form-control" style="height: 50px;" type="text" value="{todo.text}" placeholder="Enter ToDo" name="name" id="input">
                      
                      ''')



def delete_todo(request,pk):
  # htmx هتجيب التاسك صاحب الايدي وانا كتبته في 
  todo_text = Todo.objects.get(id=pk)
  # وهتحذفه
  todo_text.delete()
  # هتجيب كل التسكات ثاني وهيا دي اللي بتتمرر
  todo_all = Todo.objects.all().order_by('-id')[:7]
  context = {
    'todo_all':todo_all
  }
  return render(request,"todo.html",context)




def status_todo(request,pk):
  todo_name = Todo.objects.get(id=pk)
  if todo_name.completed == True:
    todo_name.completed = False
  else:
    todo_name.completed = True

  todo_name.save()

  # هتجيب كل التسكات ثاني وهيا دي اللي بتتمرر
  todo_all = Todo.objects.all().order_by('-id')[:7]
  context = {
    'todo_all':todo_all
  }
  return render(request,"todo.html",context)
  