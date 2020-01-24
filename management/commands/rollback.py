from django.core.management.base import BaseCommand
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Rolling back content'

    def handle(self, *args, **options):
        self.red('Are you sure?')
