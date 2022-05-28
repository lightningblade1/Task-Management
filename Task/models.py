# in general, keep your field attributes in lower-case
# check this for best practices on Django projects https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/


from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from Task.priority import CHOICES

class Folder(models.Model):
    Name=models.CharField(max_length=60,unique=True)
    def __str__(self): #This returns the name string whenever the object is called an example of this can be seen in drop down folder menu when we post tasks.Without this method it shows object(1) .With this it shows the name
        return self.Name
class Task(models.Model):
    Due_date = models.DateField()
    Folder = models.ForeignKey(Folder, on_delete=models.CASCADE, )
    Title=models.CharField(max_length=120)
    Description=models.CharField(max_length=500)
    Responsible_user=models.ManyToManyField(User)
    Priority=models.CharField(max_length=20,choices=CHOICES)
    Repeat_Days=models.PositiveIntegerField()
    Completed=models.BooleanField(default=False)


