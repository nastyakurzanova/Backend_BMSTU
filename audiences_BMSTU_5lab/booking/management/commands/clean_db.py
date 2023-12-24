from django.core.management.base import BaseCommand
from booking.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Booking.objects.all().delete()
        Audiences.objects.all().delete()