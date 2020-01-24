from abc import ABC
import csv


class BaseMapper(ABC):
    source_path = None
    source_type = None

    def __init__(self):
        self.source_path = None
        self.source_type = None

    def set_destination_file(self, path):
        self._set_source_destination(path, 'file')

    def set_destination_folder(self, path):
        self._set_source_destination(path, 'folder')

    def _set_source_destination(self, path, source_type):
        self.source_path = path
        self.source_type = source_type

    def process(self):
        if self.source_type is 'file':
            with open(self.source_path) as file:
                return self.process_single(file)
        else:
            raise NotImplemented('Process multiple files not implemented yet')

    def process_single(self, file):
        raise NotImplemented()


class CsvMapper(BaseMapper):
    delimiter = ','

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def process_single(self, file):
        results = []
        csv_reader = csv.reader(file, delimiter=self.delimiter)
        headers = next(csv_reader, None)
        for row in csv_reader:
            for h, v in zip(headers, row):
                results[h].append(v)

        print(results)


class YamlMapper(BaseMapper):
    pass


class JsonMapper(BaseMapper):
    pass


class ExcelMapper(BaseMapper):
    pass


class SqlMapper(BaseMapper):
    pass


class RestMapper(BaseMapper):
    pass


class GraphqlMapper(BaseMapper):
    pass


class PickleMapper(BaseMapper):
    pass
