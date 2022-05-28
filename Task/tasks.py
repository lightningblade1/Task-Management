from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth.models import User

from Task.models import Task, Folder



@shared_task
def Task_reapeater():
    print("hi")  # remove print statements like these from your code; never check them to you git
    Task_obj = Task.objects.filter(Completed=True)
    for i in Task_obj:
        date = i.Due_date
        Repeat_Days = i.Repeat_Days
        diff = date.today() - date
        print(type(i.Due_date))
        if int(diff.days) >= Repeat_Days:
            new_task = Task.objects.create(Title=i.Title,
                                           Folder=Folder.objects.get(id=i.Folder.id),
                                           Due_date=date.today(),
                                           Description=i.Description, Priority=i.Priority,
                                           Completed=False, Repeat_Days=i.Repeat_Days)
            users = i.Responsible_user.all()
            for user in users:
                user_obj = User.objects.get(id=int(user.id))
                new_task.Responsible_user.add(user_obj)
            new_task.save()
    return  # no need for empty return; just erase the line