from tivol.models import ContentMigrationStatus
from django.core.management.base import BaseCommand
from tivol.base_classes.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):
        entry_point = self.instance_entrypoint()

        rows = []
        for migration_handler in entry_point.migration_handlers:
            handler = migration_handler()

            rows.append([
                handler.name,
                str(self.get_number_of_migrated_items(handler.id)),
                str(self.get_number_of_items_to_migrate(handler.source_mapper))
            ])

        self.table(
            headers=[
                'Migration name',
                'Number of items',
                'Number of migrated items'
            ],
            rows=rows
        )

    def get_number_of_migrated_items(self, handler_id):
        """
        Get the number of the migrated items.

        :param handler_id: The handler ID of the migration.
        """
        return ContentMigrationStatus\
            .objects\
            .filter(handler=handler_id).count()

    def get_number_of_items_to_migrate(self, source_mapper):
        """
        Get the number of items left to migrate.

        :param source_mapper: The source mapper of the migration.
        """
        return len(source_mapper.process())
