from abc import ABC
from django.db.models import Model
from tivol.base_classes.mappers import BaseMapper
from tivol.management.helpers import SwagHelpers


class MigrationHandlerBase(ABC):
    """
    Base migration class.
    """
    name = ''
    description = ''
    source_mapper = None
    model_target = None

    def __init__(self):
        self.name = ''
        self.description = ''
        self.source_mapper = None
        self.model_target = None
        self.swag = SwagHelpers()
        self.init_metadata()

    def init_metadata(self):
        """
        Setting the metadata of the migration handler.
        """
        raise NotImplemented('The migration metadata need to be implemented')

    def set_model_target(self, model_target: Model):
        """
        Setting the model object for interaction with the DB. Invoke this one
        when in the init metadata handler.

        :param model_target: The model class reference.
        """
        self.model_target = model_target

    def add_source_mapper(self, source_mapper: BaseMapper):
        """
        Adding the source mapper. Invoke this one when in the init metadata
        handler.

        :param source_mapper: The source mapper handler.
        """
        self.source_mapper = source_mapper

    def migrate(self):
        """
        Migrating the parsed data into the DB using Django's ORM.
        """
        self.swag.blue(f'Migrating {self.name}')

        # Processing the sources.
        results = self.source_mapper.process()

        bulk_objects = []
        for result in results:
            bulk_objects.append(self.model_target(**result))

        self.model_target.objects.bulk_create(bulk_objects)
        self.swag.green(f'{self.name} migration: {len(bulk_objects)} item(s) has been migrated')
