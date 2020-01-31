from tivol.base_classes.mappers import CsvMapper
from tivol.base_classes.migration_handler_base import MigrationHandlerBase
import os


class AnimalMigration(MigrationHandlerBase):

    def init_metadata(self):
        csv_mapper = CsvMapper()
        path = os.path.join(
            os.getcwd(), 'tivol', 'tests', 'assets', 'animals.csv'
        )
        csv_mapper.set_destination_file(path=path)

        self.id = 'animal'
        self.name = 'Animal migration'
        self.description = 'Migrating animals into the system'
        self.add_source_mapper(csv_mapper)
