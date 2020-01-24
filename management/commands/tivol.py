from django.conf import settings
from django.core.management.base import BaseCommand
from pydoc import locate
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.commands.helpers import SwagHelpers


class Command(BaseCommand, SwagHelpers):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        if not hasattr(settings, 'TIVOL_ENTRY_POINT'):
            # Before we can start process something we need to know what to
            # process.
            raise AttributeError('TIVOL_ENTRY_POINT is missing in the settings')

        entry_point = locate(settings.TIVOL_ENTRY_POINT)
        if not issubclass(entry_point, EntryPoint):
            raise NotEntryPointClass(f'The {settings.TIVOL_ENTRY_POINT} is not an entry point class.')

        entry_point: EntryPoint = entry_point()

        print(entry_point.migration_handlers)

        self.black('a')
        self.red('a')
        self.green('a')
        self.yellow('a')
        self.blue('a')
        self.magenta('a')
        self.cyan('a')
        self.white('a')
        self.underline(self.black('foo', True))
