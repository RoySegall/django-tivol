from datetime import datetime
from tivol.base_classes.migration_handler_base import \
    get_destination_from_model
from tivol.base_classes.assertions import NoModelTarget
from tivol.models import ContentMigrationStatus


class PluginBase:

    def process(self, value, extra_info=None):
        """
        Convert a value to the value which the DB field expecting it to be.

        :param value: The value from the source file(s).
        :param extra_info: Additional information, i.e date format.

        :return: The value after processing.
        """
        raise NotImplemented


class DatePlugin(PluginBase):
    """
    Getting a string and transform it to a string.
    """

    def process(self, value, extra_info=None):
        return datetime.strptime(value, extra_info['format'])


class UppercasePlugin(PluginBase):
    """
    Get a string and set the first letter to be uppercase.
    """

    def process(self, value, extra_info=None):
        return value.capitalize()


class ReferencePlugin(PluginBase):
    """
    Return an ID of a migrated record based on the ID from the CSV files.

    For example, we need to migrate directors and movies. We also need to keep
    a relationship between a movie and the director of that movie. Let's look
    on two CSV files:

    directors.csv:
        id,name
        director_1,Michael Benjamin Bay
        director_2,Martin Scorsese

    Now, how should movies.csv look like? like that:
        id,name,director
        movie_1,The Wolf of Wall Street,director_2
        movie_2,The Wolf of Wall Street,director_2
        movie_3,The Departed,director_2
        movie_4,Pearl Harbor,director_1
        movie_5,Transformers,director_1
        movie_5,Transformers 2: Revenge of the Fallen,director_1

    Tivol keeps track of the ID from the source files, CSV, JSON or DB records,
    and know what is the ID of the record in the DB after the migration process
    completed.
    """

    def process(self, value, extra_info=None):
        model = extra_info.get('model')

        if not model:
            raise NoModelTarget()

        # Getting the record which tells us the ID of the migrated model based
        # on the record ID form the source files. We including also the model
        # target just in case there are two different models with the same
        # ID from the source file - a tag model object and an actor model
        # object which their source ID is "record_1" or something like this.
        results = ContentMigrationStatus.objects.get(
            source_id=value, model_target=get_destination_from_model(model)
        )

        return model.objects.get(id=results.destination_id)
