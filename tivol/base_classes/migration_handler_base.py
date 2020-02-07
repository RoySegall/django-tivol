from abc import ABC
from django.db.models import Model

from tivol.base_classes.assertions import NoModelTarget
from tivol.base_classes.mappers import BaseMapper
from tivol.management.helpers import SwagHelpers
from tivol.models import ContentMigrationStatus


def get_destination_from_model(model):
    """
    Getting the label of the model. Used for making sure we won't create
    duplicates of migrations.
    """
    return model._meta.label_lower


class MigrationHandlerBase(ABC):
    """
    Base migration class.
    """
    id = None
    name = ''
    description = ''
    source_mapper = None
    model_target = None
    fields_plugins = {}

    def __init__(self):
        self.name = ''
        self.description = ''
        self.source_mapper = None
        self.model_target = None
        self.fields_plugins = {}
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

    def prepare_values(self, row):
        """
        Iterate over the row values and apply process plugin logic.

        :param row: The row to process.
        """
        for field, plugins_metadata in self.fields_plugins.items():

            for plugin_metadata in plugins_metadata:
                process_kwargs = {}

                if isinstance(plugin_metadata, dict):
                    # That's mean that the plugin definition is a dictionary
                    # with info - which plugin we need to instantiate and what
                    # the extra info the process method is expecting.
                    plugin_instance = plugin_metadata['plugin']()

                    process_kwargs.update(
                        value=row[field],
                        extra_info=plugin_metadata['extra_info']
                    )
                else:
                    # We found a simple list of process plugin reference.
                    # We need to instantiate the referenced plugin and pass
                    # only the value to the process method.
                    plugin_instance = plugin_metadata()
                    process_kwargs['value'] = row[field]

                # Take the row and convert it to something else.
                row[field] = plugin_instance.process(**process_kwargs)

    def migrate(self):
        """
        Migrating the parsed data into the DB using Django's ORM.
        """
        # Processing the sources.
        results = self.source_mapper.process()

        if not self.model_target:
            raise NoModelTarget()

        model_label = get_destination_from_model(self.model_target)
        created_items = 0
        skipped = 0
        for result in results:

            # Go over the rows and check if we need to process the value.
            if self.fields_plugins.keys():

                if any({*self.fields_plugins.keys() & {*result.keys()}}):
                    self.prepare_values(result)

            source_id = result['id']

            # Deleting the ID key form the results. The ID help us tracking
            # if the row has been migrated or not and also help us keep
            # relationship between migrated content if we desire it.
            del result['id']

            migrated = ContentMigrationStatus.objects.filter(
                source_id=source_id, model_target=model_label,
                handler=self.id).exists()

            if migrated:
                skipped = skipped + 1
                continue

            entry = self.model_target.objects.create(**result)
            ContentMigrationStatus.objects.create(
                source_id=source_id,
                destination_id=entry.id,
                model_target=model_label,
                handler=self.id
            )
            created_items = created_items + 1

        return f'{self.name}: {created_items} migrated, {skipped} skipped'
