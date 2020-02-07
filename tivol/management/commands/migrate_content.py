import time
from django.core.management.base import BaseCommand
from tivol.base_classes.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):
        # Get the entry point instance.
        entry_point = self.instance_entrypoint()

        bar = self.progress_bar(len(entry_point.migration_handlers))

        # todo: allow option to revert specific migrations.

        self.green("Start to migrate")
        bar.start()
        for migration_handler in entry_point.migration_handlers:
            migration = migration_handler()
            bar.advance()
            time.sleep(1)
            self.green(' ' + migration.migrate())

        self.green('Migrated')
