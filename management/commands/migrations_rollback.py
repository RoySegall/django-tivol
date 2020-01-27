from clikit.io import ConsoleIO
from django.core.management.base import BaseCommand
from tivol.Assertions.assertions import NotEntryPointClass
from tivol.base_classes.entry_point import EntryPoint
from tivol.management.helpers import SwagHelpers

from clikit.ui.components import Table
from clikit.ui.style import TableStyle
from clikit.ui.style.alignment import Alignment


class Command(BaseCommand, SwagHelpers):
    help = 'Rolling back content'

    def handle(self, *args, **options):
        io = ConsoleIO()
        table = Table(TableStyle.solid())
        table.set_header_row([self.green("ISBN", True), self.green("Title", True), self.green("Author", True)])
        table.add_rows(
            [
                ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
                ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
                ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
                ["80-902734-1-6", "And Then There Were None",
                 "Agatha Christie"],
            ]
        )

        table.render(io)
