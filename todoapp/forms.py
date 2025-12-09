from . models import Task
from django import forms

class TodoForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['name', 'priority', 'task_type', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Task Name'}),
            'priority': forms.Select(attrs={'class': 'form-select custom-input'}),
            'task_type': forms.Select(attrs={'class': 'form-select custom-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control custom-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control custom-input', 'type': 'date'}),
        }