from django.db import models, connection
from django.db.models import CharField
from django.test import TestCase, TransactionTestCase
from tivol.base_classes.mappers import SqlMapper
from tivol.base_classes.mappers import CsvMapper, YamlMapper, JsonMapper
from tivol.tests.assets.mappers_for_tests import DummyMapper
import os


class OldTag(models.Model):
    """
    Dummy model. Don't mind this one.
    """
    title = CharField(max_length=255)
    description = CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        # This model is not managed by Django
        managed = False


class TestMappers(TransactionTestCase):
    """
    Testing mappers.
    """

    def setUp(self):
        """
        Creating all the custom schema which relate to test.
        """
        super().setUp()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(OldTag)

        old_tags = [
            OldTag(title="Krabby Patty", description="yummy"),
            OldTag(title="Omelette du Fromage", description="yummy"),
            OldTag(title="Chipackerz", description="yummy")
        ]

        OldTag.objects.bulk_create(old_tags)

    def tearDown(self):
        """
        Deleting all the custom schema which relate to test.
        """
        super().tearDown()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(OldTag)

    def test_set_destination_file(self):
        """
        Testing setting a single file for processing.
        """
        dummy_mapper = DummyMapper()
        dummy_mapper.set_destination_file('foo')

        self.assertEqual(dummy_mapper.source_type, 'file')
        self.assertEqual(dummy_mapper.source_path, 'foo')

    def test_set_destination_folder(self):
        """
        Testing setting a folder for processing.
        :return:
        """
        dummy_mapper = DummyMapper()
        dummy_mapper.set_destination_folder('foo')

        self.assertEqual(dummy_mapper.source_type, 'folder')
        self.assertEqual(dummy_mapper.source_path, 'foo')

    def parse_file(self, file, mapper, key=0):
        """
        Parsing a file and return the parsed content.

        :param file: The file to parse from the assets folder.
        :param mapper: The mapper to handle the file.
        :param key: Key to return. Default is 0. If set None will return all
            the object.

        :return: Parsed content.
        """
        path = os.path.join(
            os.getcwd(), 'tivol', 'tests', 'assets', file
        )

        mapper.set_destination_file(path=path)

        processed = mapper.process()
        if key is 0:
            return processed[0]
        return processed

    def test_csv_parser(self):
        """
        Testing the CSV file parser.
        """
        self.assertEqual(
            self.parse_file('animals.csv', CsvMapper()),
            {
                'id': 'animal_1',
                'animal_name': 'Cat',
                'sound': 'Meow',
                'number_of_legs': '4'
            }
        )

    def test_yaml_parser(self):
        """
        Testing the yaml file parsing.
        """
        first_row = {
            'id': 'company_1',
            'name': 'Apple',
            'description': 'Created the Mac, iPhone, iPad and more cool stuff',
            'founded_at': 'April 1, 1976',
            'founded_by': 'Steve Jobs, Steve Wozniak, Ronald Wayne'
        }
        self.assertEqual(self.parse_file('companies.yml', YamlMapper()),
                         first_row)

    def test_json_parser(self):
        """
        Testing the yaml file parsing.
        """
        first_row = {
            'birth_date': 'June 1, 1937',
            'id': 'actor_1',
            'name': 'Morgan Freeman'
        }
        self.assertEqual(self.parse_file('actors.json', JsonMapper()),
                         first_row)

    def test_sql_parser(self):
        """
        Testing the SQL parser. Mocking the db layer was a bit hard so I
        manage to bypass it by the next logic: I'm creating another model, old
        tags, and the SQL process will query that table. After that is plain
        old assertEqual.
        """

        mapper = SqlMapper()
        mapper.set_connection('default')
        mapper.set_table(OldTag._meta.db_table)
        process = mapper.process()

        first_row = {'id': 1, 'title': 'Krabby Patty', 'description': 'yummy'}
        self.assertEqual(first_row, process[0])
