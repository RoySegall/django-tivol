from django.test import TestCase
from tivol.base_classes.plugins import DatePlugin, UppercasePlugin


class TestPlugins(TestCase):

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
        pass
