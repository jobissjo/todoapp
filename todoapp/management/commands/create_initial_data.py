from django.core.management.base import BaseCommand
from todoapp.models import Priority

class Command(BaseCommand):
    help = 'Prints a hello message'

    def handle(self, *args, **options):
        Priority.objects.create(name='High', color='red')
        Priority.objects.create(name='Medium', color='yellow')
        Priority.objects.create(name='Low', color='green')
        self.stdout.write(self.style.SUCCESS('Priority added successfully'))