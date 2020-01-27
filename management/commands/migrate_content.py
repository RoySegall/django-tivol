from django.core.management.base import BaseCommand
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):

        # Get the entry point instance.
        entry_point = self.instance_entrypoint()

        self.yellow(f'Starting to migrate')
        entry_point.run_migration()
