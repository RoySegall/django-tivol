from django.conf import settings
from django.core.management.base import BaseCommand
from pydoc import locate
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):

        if not hasattr(settings, 'TIVOL_ENTRY_POINT'):
            # Before we can start process something we need to know what to
            # process.
            raise AttributeError('TIVOL_ENTRY_POINT is missing in the settings')

        entry_point_class = locate(settings.TIVOL_ENTRY_POINT)
        if not issubclass(entry_point_class, EntryPoint):
            raise NotEntryPointClass(f'The {settings.TIVOL_ENTRY_POINT} is not an entry point class.')

        # Init the entry point class and run the migrations.
        entry_point: EntryPoint = entry_point_class()

        self.yellow(f'Starting to migrate')
        entry_point.run_migration()