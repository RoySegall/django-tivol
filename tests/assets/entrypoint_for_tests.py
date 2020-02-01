from tivol.base_classes.entry_point import EntryPoint
from .migration_handlers import AnimalMigration


class FailingEntryPointForTests(EntryPoint):
    """
    This class won't hold any thing. In order to fail.
    """
    pass


class EntryPointForTests(EntryPoint):
    """
    This class will hold reference for other migrations.
    """

    def register_migrations(self):
        self.add_migration_handler(AnimalMigration)
