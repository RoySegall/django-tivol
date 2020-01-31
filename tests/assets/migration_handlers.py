from tivol.base_classes.mappers import CsvMapper
from tivol.base_classes.migration_handler_base import MigrationHandlerBase
import os


class AnimalMigration(MigrationHandlerBase):

    def init_metadata(self):
        csv_mapper = CsvMapper()
        csv_mapper.set_destination_file(path=os.path.join(os.getcwd(), 'dummyapp', 'tivol_migrations', 'source_files', 'animals.csv'))

        self.id = 'animal'
        self.name = 'Animal migration'
        self.description = 'Migrating animals into the system'
        self.add_source_mapper(csv_mapper)
