from abc import ABC
from tivol.base_classes.migration_handler_base import MigrationHandlerBase


class EntryPoint(ABC):
    """
    This is the entry point which describes the migration workflow.
    """

    def __init__(self):
        self.register_migrations()
        self.migration_handlers = []

    def register_migrations(self):
        """
        In this method, we'll introduce our migrations. The registered mappers
        will tell tivol which migrations handlers we want to execute.
        :return:
        """
        raise NotImplementedError('You need to register your migration mappers')

    def add_migration_handler(self, handler: MigrationHandlerBase):
        """
        Using this method we going to add migration handlers. Each migration
        handler has a couple of organs.

        The first one is the source folder\file. a source folder holds list of
        files which then mapped into objects. A source file can holds a bunch of
        rows which then mapped into objects. After we got the object we can
        insert then in a bulk in to the DB.

        The second, is the source mapper. The source mapper can handle a
        specific type of file or folder, i.e CSV file or a list of JSON files,
        and then parse the data into the DB.


        :param handler:
        """
        pass
