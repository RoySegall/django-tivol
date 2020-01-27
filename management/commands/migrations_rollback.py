from clikit.io import ConsoleIO
from django.core.management.base import BaseCommand
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers
from tivol.models import ContentMigrationStatus
from clikit.ui.components import ProgressBar
import time


class Command(BaseCommand, SwagHelpers):
    help = 'Rolling back content'

    def handle(self, *args, **options):
        self.red('Sure?')
