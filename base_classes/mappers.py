from abc import ABC
import csv
import yaml


class BaseMapper(ABC):
    """
    This is the base mapper class. Any source mapper will need to extend this
    one.

    A source mapper is a small logic unit which read data from a file, or a list
    of files(depends on the logic we want to implement), and parse the data into
    data which can be handled by Django's ORM.
    """
    source_path = None
    source_type = None

    def __init__(self):
        self.source_path = None
        self.source_type = None

    def set_destination_file(self, path):
        """
        Setting a file as our data source.

        :param path: The path of the file.
        """
        self._set_source_destination(path, 'file')

    def set_destination_folder(self, path):
        """
        Setting a folder as our data source. In this case, all the files in the
        folder will be handled as a source file.

        :param path: The path of the folder.
        """
        self._set_source_destination(path, 'folder')

    def _set_source_destination(self, path, source_type):
        """
        Helper function to set the source data.
        :param path: The path of the source.
        :param source_type: The type of the source - file\folder path or maybe
        MySQL database.
        """
        self.source_path = path
        self.source_type = source_type

    def process(self):
        """
        Processing the data from the source data.
        """
        if self.source_type is 'file':
            with open(self.source_path) as file:
                return self.process_single(file)
        else:
            raise NotImplemented('Process multiple files not implemented yet')

    def process_single(self, file):
        """
        Base class for processing a single file.

        :param file: The file to handle.
        """
        raise NotImplemented()


class CsvMapper(BaseMapper):
    """
    Processing CSV file into array of objects.
    """
    delimiter = ','

    def __init__(self):
        super().__init__()
        self.delimiter = ','

    def process_single(self, file):
        results = []
        csv_reader = csv.reader(file, delimiter=self.delimiter)
        headers = next(csv_reader, None)

        for row in csv_reader:
            row_dictionary = {}

            for key, value in zip(headers, row):
                if key == 'id':
                    # The id is used for tracking the values form the source
                    # file so we could later on rollback or maybe update a
                    # migrated row.
                    continue

                row_dictionary[key.strip()] = value

            results.append(row_dictionary)

        return results


class YamlMapper(BaseMapper):

    def process_single(self, file):
        return yaml.load(file, Loader=yaml.FullLoader)


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
