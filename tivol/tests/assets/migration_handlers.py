from tivol.base_classes.mappers import CsvMapper
from tivol.base_classes.migration_handler_base import MigrationHandlerBase
import os


class CsvMapperTests(CsvMapper):

    def __init__(self):
        super().__init__()
        self.hook_pre_processing_file = False
        self.hook_post_processing_file = False

    def hook_pre_processing_file(self, file):
        self.hook_pre_processing_file = True

    def hook_post_processing_file(self, results):
        self.hook_post_processing_file = True


class AnimalMigration(MigrationHandlerBase):

    def __init__(self):
        super().__init__()
        self.hook_pre_process_files_called = False
        self.hook_post_process_files_called = False
        self.hook_pre_insert_record_called = False
        self.hook_post_insert_record_called = False

    def init_metadata(self):
        csv_mapper = CsvMapperTests()
        path = os.path.join(
            os.getcwd(), 'tivol', 'tests', 'assets', 'animals.csv'
        )
        csv_mapper.set_destination_file(path=path)

        self.id = 'animal'
        self.name = 'Animal migration'
        self.description = 'Migrating animals into the system'
        self.add_source_mapper(csv_mapper)

    def hook_pre_process_files(self, migration_class):
        self.hook_pre_process_files_called = True

    def hook_post_process_files(self, files):
        self.hook_post_process_files_called = True

    def hook_pre_insert_record(self, properties, model):
        self.hook_pre_insert_record_called = True

    def hook_post_insert_record(self, properties, model):
        self.hook_post_insert_record_called = True
