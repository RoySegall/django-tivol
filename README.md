# Tivol
Welcome to Tivol. You probably wonder to your self 
"what's this Django app do?". Let's start with a scenario. You created 
your Django site, or backend and you start to insert data which you can 
work with. After a while two things came up:
1. Someone new joined your team and the new guy has no data to work with
2. You set up a CI with selenium and you need to run e2e tests which 
means you need to create data during the tests

There are more scenarios but all of them comes to the same point - you 
need real life data. 

This is where tivol come handy, you can keep data in source files and 
insert them to the DB thus allow you to work on dummy content without 
any problem.

We'll cover up later on how to develop features in your project with a 
DOD(Data Oriented Development) approach but first, let's see how to 
integrated you Django project with Tivol. 

## Setup
First, we need to register the map. We can do this by adding it to the 
installed app list:
```
INSTALLED_APPS = [
    ...
    'tivol.apps.TivolConfig',
]
```

After that, we'll need to register a "Migration entry point". Migration 
entry point tells to the tivol package the migration handlers we create. 
The migration handlers will eventually take data from a source file, or 
a folder, and will insert them to the DB.

First, you'll need to create an entry point class:

```python
from tivol.base_classes.entry_point import EntryPoint


class CustomEntryPoint(EntryPoint):

    def register_migrations(self):
        pass
```

It's recommended to create a folder, i.e `tivol_migration`, and holds 
there the data and the migrations handlers(which will be covered later 
on).

After we created out custom entry point, you'll need to register it like
that:

```python
TIVOL_ENTRY_POINT = 'path.to.the.CustomEntryPoint'
```

## Migrate content
After registering the entry point, we need to introduced our data files
to the Tivol application. 

### Register migration handlers
Write here how to add migration handler.


```python
from dummyapp.tivol_migrations.animals_migration import AnimalMigrations
from tivol.base_classes.entry_point import EntryPoint


class CustomEntryPoint(EntryPoint):

    def register_migrations(self):
        self.add_migration_handler(AnimalMigrations)
```

### Write data mappers
Write here how to interact with the mappers and the other elements:

```python
class AnimalMigrations(MigrationHandlerBase):

    def init_metadata(self):
        csv_mapper = CsvMapper()
        csv_mapper.set_destination_file(path=os.path.join(os.getcwd(), 'dummyapp', 'tivol_migrations', 'source_files', 'animals.csv'))

        self.name = 'Animal migration'
        self.description = 'Migrating animals into the system'
        self.add_source_mapper(csv_mapper)
        self.set_model_target(Animal)
```

## Tivol CLI commands

### Migrate content
```bash
python manage.py migrate_content
```
