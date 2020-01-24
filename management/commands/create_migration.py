from django.core.management.base import BaseCommand
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Creating migration files'

    def handle(self, *args, **options):
        self.green('Creating migration...')
