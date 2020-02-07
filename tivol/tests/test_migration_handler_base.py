from django.test import TransactionTestCase
from tivol.base_classes.assertions import NoModelTarget
from tivol.base_classes.mappers import CsvMapper
from tivol.base_classes.plugins import UppercasePlugin
from tivol.tests.assets.migration_handlers import AnimalMigration
from django.db import connection, models
from django.db.models import CharField, IntegerField


class Animal(models.Model):
    animal_name = CharField(max_length=25)
    sound = CharField(max_length=25)
    number_of_legs = IntegerField()

    def __str__(self):
        return self.animal_name

    class Meta:
        # This model is not managed by Django
        managed = False


class TestMigrationHandlerBase(TransactionTestCase):
    """
    Testing the migration section.
    """

    def setUp(self):
        """
        Creating all the custom schema which relate to test.
        """
        super().setUp()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Animal)

        self.migration = AnimalMigration()

    def tearDown(self):
        """
        Deleting all the custom schema which relate to test.
        """
        super().tearDown()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(Animal)

    def test_set_model_target(self):
        """
        Testing setting the model target.
        """
        self.migration.set_model_target(Animal)
        self.assertEqual(self.migration.model_target, Animal)

    def test_add_source_mapper(self):
        """
        Testing setting the model target.
        """
        self.assertIsInstance(self.migration.source_mapper, CsvMapper)

    def test_prepare_values(self):
        """
        Testing the prepare values method.
        """

        class UppercasePluginDummy(UppercasePlugin):

            def process(self, value, extra_info=None):
                raise AssertionError('Raising so we could catch it')

        self.migration.fields_plugins = {
            'name': [UppercasePluginDummy],
        }

        try:
            self.migration.prepare_values({'name': 'foo'})
            self.fail('Our process function has not been invoked')
        except AssertionError as e:
            self.assertEqual(str(e), 'Raising so we could catch it')

    def test_migrate(self):
        """
        Testing migration into the DB.
        """
        self.assertEqual(0, Animal.objects.count())
        try:
            self.migration.migrate()
            self.fail()
        except NoModelTarget as e:
            pass

        self.migration.set_model_target(Animal)
        self.migration.migrate()
        self.assertEqual(7, Animal.objects.count())
        Animal.objects.get(animal_name='Cat')
