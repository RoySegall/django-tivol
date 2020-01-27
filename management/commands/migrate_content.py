from clikit.ui.components import ProgressBar
import time
from clikit.io import ConsoleIO
from django.core.management.base import BaseCommand
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):
        io = ConsoleIO()

        # Get the entry point instance.
        entry_point = self.instance_entrypoint()
        bar = ProgressBar(io, len(entry_point.migration_handlers))
        bar.set_bar_character("■")
        bar.set_progress_character('')

        self.green("Start to migrate \n")
        bar.start()

        for migration_handler in entry_point.migration_handlers:
            migration = migration_handler()
            bar.advance()
            time.sleep(1)
            self.green(' ' + migration.migrate())

        print("\n")
        self.green('Migrated')
