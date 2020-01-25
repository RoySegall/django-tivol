from datetime import datetime


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
