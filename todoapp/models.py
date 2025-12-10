from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Priority(models.Model):
    name=models.CharField(max_length=250)
    color=models.CharField(max_length=250)

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('one_time','One Time'),
        ('recurring','Recurring'),
    ]
    name=models.CharField(max_length=250)
    priority=models.ForeignKey(Priority,on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)
    completed_date=models.DateTimeField(null=True,blank=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    is_active=models.BooleanField(default=False)
    task_type=models.CharField(max_length=250,choices=TASK_TYPE_CHOICES, default='one_time')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name



class TaskLog(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    completed_date=models.DateTimeField(null=True,blank=True)
    is_completed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.task.name