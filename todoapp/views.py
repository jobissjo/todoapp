from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TodoForm
from .models import Task, Priority
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'

    def get_queryset(self):
        return Task.objects.filter(is_completed=False)
class TaskDetailView(DetailView):
    model= Task
    template_name = 'details.html'
    context_object_name = 'task'
class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ['name', 'priority', 'task_type', 'start_date', 'end_date']
    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk':self.object.id})
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('cbvhome')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Mark as done logic (similar to function view below)
        from .models import TaskLog
        import datetime
        
        # Log completion
        TaskLog.objects.create(
            task=self.object,
            date=datetime.date.today(),
            is_completed=True,
            completed_at=datetime.datetime.now()
        )

        if self.object.task_type == 'one_time':
            self.object.is_completed = True
            self.object.completed_at = datetime.datetime.now()
            self.object.save()
        
        # If recurring, we don't mark the main task as completed, just the log.
        # But since this is a "DeleteView" that usually redirects, we redirect.
        # Note: We are overriding delete to NOT delete from DB.
        
        return redirect(self.success_url)

# Create your views here.
def add(request):
    task1 = Task.objects.filter(is_completed=False)
    if request.method=="POST":
        name=request.POST.get('task','')
        priority_id=request.POST.get('priority','')
        start_date=request.POST.get('start_date','')
        end_date=request.POST.get('end_date','') # Assuming end date is provided or logic needed
        task_type=request.POST.get('task_type','one_time')
        
        if end_date == '':
            end_date = start_date # Fallback

        if priority_id:
             priority = Priority.objects.get(id=priority_id)
             task=Task(name=name, priority=priority, start_date=start_date, end_date=end_date, task_type=task_type)
             task.save()

    return render(request,'home.html', {'task1': task1, 'priorities': Priority.objects.all()})
def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        from .models import TaskLog
        import datetime
        
        TaskLog.objects.create(
            task=task,
            date=datetime.date.today(),
            is_completed=True,
            completed_at=datetime.datetime.now()
        )

        if task.task_type == 'one_time':
            task.is_completed = True
            task.completed_at = datetime.datetime.now()
            task.save()
            
        return redirect('/')

    return render(request, 'delete.html')
def update(request,id):
    task=Task.objects.get(id=id)
    form1=TodoForm(request.POST or None, instance=task)
    if form1.is_valid():
        form1.save()
        return redirect('/')
    return render(request,'edit.html',{'form1':form1,'task':task})