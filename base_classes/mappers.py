from abc import ABC


class BaseMapper(ABC):
    pass


class CsvMapper(BaseMapper):
    pass


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
