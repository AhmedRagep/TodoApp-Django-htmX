from django.shortcuts import redirect, render
from .models import Todo,Contact
from django.http import HttpResponse
from .forms import ContactForm
from django.utils.html import format_html
# Create your views here.



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
  


def contact(request):
  return render(request, 'contact_all.html',{"form":ContactForm(),'contacts':Contact.objects.all().order_by('-id')[:9]})


def create_contact(request):
  if request.POST:
    form = ContactForm(request.POST or None)
    if form.is_valid():
      # جلب البيان المنشأ في متغير
      contactname = form.save()
      # ارساله لصفحة البيان الواحد
      return render(request,'contact_list.html',{'contact':contactname})
  # وهنا ارسال الفورم فارغه لكي تظهر عند اضافة جديد
  return render(request,'contact.html',{'form':ContactForm()})



def delete_contact(request,pk):
  # htmx هتجيب التاسك صاحب الايدي وانا كتبته في 
  contact_get = Contact.objects.get(id=pk)
  # وهتحذفه
  contact_get.delete()
  # هتجيب كل التسكات ثاني وهيا دي اللي بتتمرر
  contacts = Contact.objects.all().order_by('-id')[:9]

  context = {
    'form':ContactForm(),
    'contacts':contacts
  }
  return render(request,"contact_all.html",context)



# جلب عدد البيانات جميعا
def search_view(request):
    all_contact = Contact.objects.all()
    context = {'count': all_contact.count()}
    return render(request, 'search.html', context)

# دالة البحث
def search_results_view(request):
    # جلب البحث
    query = request.GET.get('search', '')
    # جلب جميع البيانات
    all_contact = Contact.objects.all()
    # لو البحث فيه كلام
    if query:
        # متغير بيه فلتر بالكلام اللي ببحث عنه
        contact_name = all_contact.filter(name__icontains=query)
        # جلب الكلام من البحث وعمل لون عليه من الدالة اللتي في الاسفل
        highlighted_contact_name = [{
           'name': highlight_matched_text(Contact.name, query),
           'phone_number': highlight_matched_text(Contact.phone_number, query)}
            for Contact in contact_name]
    else:
        highlighted_contact_name = []

    # ارجع لي بالبيانات اللي جت من متغير اللون وكمان عدد النتائج
    context = {'contact_name': highlighted_contact_name, 'count': all_contact.count()}
    return render(request, 'search_results.html', context)


def highlight_matched_text(text, query):
    # يبحث عن موقع أول ظهور للكلمة المستهدفة في النص وتصغيرها
    start = text.lower().find(query.lower())
    # إذا لم يتم العثور على الكلمة المستهدفة، يتم إرجاع النص كما هو دون أي تغيير
    if start == -1:
        return text
    # حساب نهاية الكلمة المستهدفة في النص
    end = start + len(query)
    # إنشاء نص مميز يتضمن الكلمة المستهدفة داخل عنصر <span> مع فئة highlight
    # هذه الفئه موجودة في صفحة العرض
    highlighted = format_html('<span class="highlight">{}</span>', text[start:end])
    # إرجاع النص الجديد الذي يتضمن الجزء الأول من النص قبل الكلمة المستهدفة، والجزء المميز، والجزء الباقي من النص بعد الكلمة المستهدفة
    return format_html('{}{}{}', text[:start], highlighted, text[end:])