import json
from abc import ABC
import csv
import yaml
from django.db import connections
from tivol.base_classes.assertions import OtherConnectionNotSet, \
    SourceTableNotSet, RestRequestFailed, RequestAddressNotSet
import requests
from requests import status_codes


class BaseMapper(ABC):
    """
    This is the base mapper class. Any source mapper will need to extend this
    one.

    A source mapper is a small logic unit which read data from a file, or a
    list of files(depends on the logic we want to implement), and parse the
    data into data which can be handled by Django's ORM.
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
        if self.source_type == 'file':
            # Go over a single file.
            with open(self.source_path) as file:
                return self.process_single(file)

        if self.source_type == 'folder':
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
                row_dictionary[key.strip()] = value

            results.append(row_dictionary)

        return results


class YamlMapper(BaseMapper):

    def process_single(self, file):
        return yaml.load(file, Loader=yaml.FullLoader)


class JsonMapper(BaseMapper):
    def process_single(self, file):
        return json.load(file)


class SqlMapper(BaseMapper):

    connection = None
    table = None

    def __init__(self):
        super().__init__()
        self.connection = None
        self.table = None

    def set_connection(self, connection_name):
        """
        Connecting to other database using Django's database layer. After
        defining another connection in the settings this mehod will tell the
        mapper which connection it should use.

        :param connection_name: The connection name.
        """
        self.connection = connection_name
        return self

    def set_table(self, table_name):
        """
        The table name to pull data from.
        """
        self.table = table_name
        return self

    def process(self):
        if not self.connection:
            raise OtherConnectionNotSet()

        if not self.table:
            raise SourceTableNotSet()

        with connections[self.connection].cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table}")

            columns = [column[0] for column in cursor.description]

            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

        return results


class RestMapper(BaseMapper):

    address = ''

    def __init__(self):
        super().__init__()
        self.address = ''

    def set_address(self, address):
        """
        Setting the address

        :param address: The address to pull data from.
        """
        self.address = address

    def process(self):

        if not self.address:
            raise RequestAddressNotSet()

        response = requests.get(self.address)

        if response.status_code != status_codes.codes.ALL_OK:
            raise RestRequestFailed()

        # Return the response.
        return response.json()
