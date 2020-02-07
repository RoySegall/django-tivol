from django.conf import settings
from pydoc import locate
from tivol.base_classes.assertions import NotEntryPointClass, \
    EntryPointIsMissing
from tivol.base_classes import entry_point
from clikit.io import ConsoleIO
from clikit.ui.components import ProgressBar, Question, ConfirmationQuestion, \
    Table, ChoiceQuestion
from clikit.ui.style import TableStyle


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

    def confirmation_question(self, question):
        q = Question(question)
        cq = ConfirmationQuestion(question=q.question)
        return cq.ask(self.io())

    def question_with_options(self, question, options, multi=False):
        q = Question(question)
        cq = ChoiceQuestion(q.question, options)
        cq.set_multi_select(multi)
        return cq.ask(self.io())

    def table(self, headers=None, rows=None):
        table = Table(TableStyle.solid())
        table.set_header_row(headers)
        table.add_rows(rows)
        table.render(self.io())

    def io(self):
        return ConsoleIO()

    def progress_bar(self, items) -> ProgressBar:
        bar = ProgressBar(self.io(), items)
        bar.set_bar_character("■")
        bar.set_progress_character('')
        return bar

    def instance_entrypoint(self):
        """
        Get the entry point instance.
        """
        if not hasattr(settings, 'TIVOL_ENTRY_POINT'):
            # Before we can start process something we need to know what to
            # process.
            raise EntryPointIsMissing()

        entry_point_class = locate(settings.TIVOL_ENTRY_POINT)
        if not issubclass(entry_point_class, entry_point.EntryPoint):
            raise NotEntryPointClass()

        # Init the entry point class and run the migrations.
        return entry_point_class()
