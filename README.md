# Tivol
Welcome to `Tivol`. You probably wonder to your self "what's this Django 
app do?". Let's start with a scenario. You created your Django site, or 
backend and you start to insert data which you can work with. After a 
while two things came up:
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
integrated you Django project with `Tivol`. 

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
to the `Tivol` application. There are two steps for this process(for 
each migration content migration type).

### Register migration handlers
First, we need register the migration handler. Remember the entry point
you created earlier? Awesome, go there. You can register the migration 
handler by using the method `add_migration_handler`. It suppose to look 
like this:

```python
from dummyapp.tivol_migrations.animals_migration import AnimalMigrations
from tivol.base_classes.entry_point import EntryPoint


class CustomEntryPoint(EntryPoint):

    def register_migrations(self):
        self.add_migration_handler(AnimalMigrations)
```

Notice that we only register the class reference and not instantiating 
it. This will be done when migrating the content but don't worry - this
is not you task.

The class we referencing to will provide information for `Tivol` about 
the migration: where is the source of our data, which source mapper will 
handle the data and much more. It's also providing for us migration life
cycle hooks - before content migration, after content migration end much 
more. We'll discuss it in the future.

### Write data mappers
This is where the magic happens. We going to inspect the class we 
registered as a migration handler. Let's look first on the code:

```python
class AnimalMigrations(MigrationHandlerBase):

    def init_metadata(self):
        self.name = 'Animal migration'
        self.description = 'Migrating animals into the system'
        
        csv_mapper = CsvMapper()
        csv_mapper.set_destination_file(path=os.path.join(os.getcwd(), 'dummyapp', 'tivol_migrations', 'source_files', 'animals.csv'))
        self.add_source_mapper(csv_mapper)

        self.set_model_target(Animal)
```

The migration handler extends from the `MigrationHandlerBase`. For the 
basic migration workflow we need to use the `init_metadata`, as you 
already saw, and there's a couple of code section that we need to 
discuss about:

```python
self.name = 'Animal migration'
self.description = 'Migrating animals into the system'
```
In this part we described the migration and what's it going to do.

```python
csv_mapper = CsvMapper()
csv_mapper.set_destination_file(path=os.path.join(os.getcwd(), 'dummyapp', 'tivol_migrations', 'source_files', 'animals.csv'))
self.add_source_mapper(csv_mapper)
```

In this part we created an instance of the `CsvMapper`, specified the 
path of the CSV file and registered it. `Tivol` need this one so we
could get data from the file(s) and insert them to the DB. 

The last is the, `self.set_model_target(Animal)` which tells `Tivol` 
what is the DB model object. Again, don't pass the instantiated object
but the reference to the object.s   

## Tivol CLI commands
Let's go over some CLI commands we get out of the box:

### Migrate content
So you create content and now you to import it in? No problem. Just hit:
```bash
python manage.py migrate_content
```

You'll get something like this:
```cli
Starting to migrate
Migrating Animal migration
Animal migration migration: 7 item(s) has been migrated
```

## Extra info
If you want to look at some examples or some blog post look the next 
list: 
* [Dummy app](https://github.com/RoySegall/tivol-dummy-app) - holds 
examples for the feature `Tivol` has to offer
