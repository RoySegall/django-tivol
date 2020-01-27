from tabulate import tabulate
from django.conf import settings
from pydoc import locate
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes import entry_point


class SwagHelpers:
    def color_text(self, text, color):
        colors = {
            'black': '30',
            'red': '31',
            'green': '32',
            'yellow': '33',
            'blue': '34',
            'magenta': '35',
            'cyan': '36',
            'white': '37',
            'underline': '4',
        }
        return f'\033[{colors[color]}m{text}\033[0m'

    def black(self, text, return_text=False):
        text = self.color_text(text, 'black')

        if return_text:
            return text

        print(text)

    def green(self, text, return_text=False):
        text = self.color_text(text, 'green')

        if return_text:
            return text

        print(text)

    def red(self, text, return_text=False):
        text = self.color_text(text, 'red')

        if return_text:
            return text

        print(text)

    def yellow(self, text, return_text=False):
        text = self.color_text(text, 'yellow')

        if return_text:
            return text

        print(text)

    def blue(self, text, return_text=False):
        text = self.color_text(text, 'blue')

        if return_text:
            return text

        print(text)

    def magenta(self, text, return_text=False):
        text = self.color_text(text, 'magenta')

        if return_text:
            return text

        print(text)

    def cyan(self, text, return_text=False):
        text = self.color_text(text, 'cyan')

        if return_text:
            return text

        print(text)

    def white(self, text, return_text=False):
        text = self.color_text(text, 'white')

        if return_text:
            return text

        print(text)

    def underline(self, text, return_text=False):
        text = self.color_text(text, 'underline')

        if return_text:
            return text

        print(text)

    def question(self):
        pass

    def table(self, headers=None, rows=None):
        print(tabulate(
            headers=headers,
            tabular_data=rows,
            tablefmt='fancy_grid',
            numalign="left"
        ))

    def autocomplete(self):
        pass

    def instance_entrypoint(self):
        """
        Get the entry point instance.
        """
        if not hasattr(settings, 'TIVOL_ENTRY_POINT'):
            # Before we can start process something we need to know what to
            # process.
            raise AttributeError('TIVOL_ENTRY_POINT is missing in the settings')

        entry_point_class = locate(settings.TIVOL_ENTRY_POINT)
        if not issubclass(entry_point_class, entry_point.EntryPoint):
            raise NotEntryPointClass(f'The {settings.TIVOL_ENTRY_POINT} is not an entry point class.')

        # Init the entry point class and run the migrations.
        return entry_point_class()
