from django.test.testcases import TestCase
from tivol.base_classes.assertions import MigrationsNotRegistered
from tivol.tests.assets.entrypoint_for_tests import FailingEntryPointForTests,\
    EntryPointForTests
from tivol.tests.assets.migration_handlers import AnimalMigration


class TestEntryPoint(TestCase):
    """
    Test the entry point class logic.
    """

    def test_register_migrations(self):
        """
        should raise an exception.
        """
        try:
            FailingEntryPointForTests()
            self.fail()
        except MigrationsNotRegistered as e:
            pass

    def test_add_migration_handler(self):
        """
        Testing the migration handler are being added to the objects.
        """
        valid_entry_point = EntryPointForTests()
        self.assertEqual(
            valid_entry_point.migration_handlers, [AnimalMigration]
        )
