from tivol.models import ContentMigrationStatus
from clikit.io import ConsoleIO
from django.core.management.base import BaseCommand
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers
from clikit.ui.components import Table
from clikit.ui.style import TableStyle


class Command(BaseCommand, SwagHelpers):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):
        entry_point = self.instance_entrypoint()

        io = ConsoleIO()
        table = Table(TableStyle.solid())
        table.set_header_row(['Migration name', 'Number of items', 'Number of migrated items'])

        for migration_handler in entry_point.migration_handlers:
            handler = migration_handler()

            table.add_row([
                handler.name,
                str(self.get_number_of_migrated_items(handler.id)),
                str(self.get_number_of_items_to_migrate(handler.source_mapper))
            ])

        table.render(io)

    def get_number_of_migrated_items(self, handler_id):
        """
        Get the number of the migrated items.

        :param handler_id: The handler ID of the migration.
        """
        return ContentMigrationStatus.objects.filter(handler=handler_id).count()

    def get_number_of_items_to_migrate(self, source_mapper):
        """
        Get the number of items left to migrate.

        :param source_mapper: The source mapper of the migration.
        """
        return len(source_mapper.process())
