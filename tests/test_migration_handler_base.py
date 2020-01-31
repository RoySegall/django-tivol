from django.test import TransactionTestCase
from tivol.tests.assets.migration_handlers import AnimalMigration
from .models import Animal
from django.db import connection


class TestMigrationHandlerBase(TransactionTestCase):
    """
    Testing the migration section.
    """

    def setUp(self):
        super().setUp()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Animal)

    def tearDown(self):
        super().tearDown()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(Animal)

    def test_set_model_target(self):
        animal_migration = AnimalMigration()
        animal_migration.set_model_target(Animal)
        self.assertEquals(animal_migration.model_target, Animal)

    def test_add_source_mapper(self):
        pass

    def test_prepare_values(self):
        pass

    def test_migrate(self):
        pass
