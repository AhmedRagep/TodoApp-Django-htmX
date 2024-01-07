from django.db import models

# Create your models here.

class Todo(models.Model):
  text = models.TextField()
  completed = models.BooleanField(default=False)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.text[:40]
  
  class Meta:
     verbose_name_plural = 'test name'



class Contact(models.Model):
  name = models.CharField(max_length=30)
  phone_number = models.CharField(max_length=50)

  def __str__(self):
      return self.name