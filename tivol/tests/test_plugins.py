from django.test import TransactionTestCase
from tivol.models import ContentMigrationStatus
from tivol.base_classes.plugins import DatePlugin, UppercasePlugin, \
    ReferencePlugin
from tivol.base_classes.migration_handler_base import \
    get_destination_from_model
from django.db import models, connection


class Director(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        # This model is not managed by Django.
        managed = False


class TestPlugins(TransactionTestCase):

    def setUp(self):
        """
        Creating all the custom schema which relate to test.
        """
        super().setUp()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Director)

    def tearDown(self):
        """
        Deleting all the custom schema which relate to test.
        """
        super().tearDown()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(Director)

    def test_date_plugin(self):
        """
        Testing the date plugin.
        """
        date_plugin = DatePlugin()
        parsed = date_plugin.process('April 1, 1976', {'format': '%B %d, %Y'})
        self.assertEqual(parsed.year, 1976)
        self.assertEqual(parsed.month, 4)
        self.assertEqual(parsed.day, 1)

    def test_uppercase_plugin(self):
        """
        Testing the upper case plugin.
        """
        date_plugin = UppercasePlugin()
        parsed = date_plugin.process('pizza')
        self.assertEqual(parsed, 'Pizza')

    def test_reference_plugin(self):
        """
        Testing the reference plugin.
        """
        reference_plugin = ReferencePlugin()

        try:
            reference_plugin.process('director_1', {'model': Director})
        except ContentMigrationStatus.DoesNotExist as e:
            self.assertEqual(
                'ContentMigrationStatus matching query does not exist.',
                str(e)
            )

        director = Director.objects.create(name='George Lucas')

        ContentMigrationStatus.objects.create(
            source_id='director_1',
            destination_id=director.id,
            model_target=get_destination_from_model(Director)
        )

        results = reference_plugin.process('director_1', {'model': Director})
        self.assertEqual(results, director)
