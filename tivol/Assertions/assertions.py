class NotEntryPointClass(Exception):
    pass


class EntryPointIsMissing(Exception):
    pass


class MigrationsNotRegistered(Exception):
    pass


class NoModelTarget(Exception):
    pass


class OtherConnectionNotSet(Exception):
    pass


class SourceTableNotSet(Exception):
    pass
