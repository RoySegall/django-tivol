from abc import ABC
from django.db.models import Model
from tivol.base_classes.mappers import BaseMapper
from tivol.management.helpers import SwagHelpers


class MigrationHandlerBase(ABC):
    name = ''
    description = ''
    source_mapper = None
    model_target = None

    def __init__(self):
        self.name = ''
        self.description = ''
        self.source_mapper = None
        self.init_metadata()
        self.model_target = None
        self.swag = SwagHelpers()

    def init_metadata(self):
        raise NotImplemented('The migration metadata need to be implemented')

    def set_model_target(self, model_target: Model):
        self.model_target = model_target

    def add_source_mapper(self, source_mapper: BaseMapper):
        self.source_mapper = source_mapper

    def migrate(self):
        self.swag.blue(f'Migrating {self.name}')

        # Processing the sources.
        self.source_mapper.process()
