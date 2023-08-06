from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from app.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        for i in range(total):
            User.objects.create(username=fake.user_name(), email=fake.email(), password=get_random_string())