# Tivol
Welcome to `Tivol`. You probably wonder to your self "what's this Django
app do?". Let's start with a scenario: you created your Django site, or
a backend with REST framework and you start to insert data which you
work with. After a while two things came up:
1. Someone new joined your team and the new guy has no data to work with
2. You set up a CI with selenium and you need to run e2e tests which
means you need to create data during the tests

There are more scenarios but all of them comes to the same point - you
need real life data.

This is where `tivol` come handy, you can keep data in source files and
insert them to the DB thus allow you to work on dummy content without
any problem.

We'll cover up later on how to develop features in your project with a
DOD (Data Oriented Development) approach but first, let's see how to
integrated your Django project with `Tivol`.

## Setup
First, we need to register the map. We can do this by adding it to the
installed app list:
```
INSTALLED_APPS = [
    ...
    'tivol',
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
there the data and the migrations handlers (which will be covered later
on).

After we created out custom entry point, you'll need to register it like
that:

```python
TIVOL_ENTRY_POINT = 'path.to.the.CustomEntryPoint'
```

## Migrate content
After registering the entry point, we need to introduce our data files
to the `Tivol` application. There are two steps for this process. This
process will repeat it self each time you want to add more content
migrations.

### Register migration handlers
First, we need register the migration handler. Remember the entry point
you created earlier? Awesome, go there. You can register the migration
handler by using the method `add_migration_handler`. It suppose to look
like this:

```python
from dummyapp.tivol_migrations.animals_migration import AnimalMigration
from dummyapp.tivol_migrations.companies_migration import CompanyMigration
from tivol.base_classes.entry_point import EntryPoint


class CustomEntryPoint(EntryPoint):

    def register_migrations(self):
        self.add_migration_handler(AnimalMigration)
        self.add_migration_handler(CompanyMigration)
```

Notice that we only register the class reference and not instantiating
it.

The class we're referencing will provide information for `Tivol` about
the migration: where is the source of our data, which source mapper will
handle the data and much more. It's also provides for us `migration life
cycle hooks` - before content migration, after content migration end
much more. We'll discuss it in the future.

### How to write a migration source
Well... there is no actual rule except for one thing: each row,
collection of values we want to import, must have an ID. This used for
not importing the same data twice and to have to ability to rollback the
migrated content from the DB. For more examples - have a look [here](https://github.com/RoySegall/tivol-dummy-app/tree/master/tivol_migrations/source_files)

### Writing source mapper
Source mapper is something that take data from one place and then return
a list dictionaries which then can be inserted to the DB using Django's
ORM (but this part is not your responsibility). Let's look on the Yaml
source mapper, since it's the smallest one:

```python
class YamlMapper(BaseMapper):

    def process_single(self, file):
        return yaml.load(file, Loader=yaml.FullLoader)
```

The only logic that relate for processing data from a place and return
it is the `process_single` method. That method will be invoke in case of
a single file or a directory. No need to worry about how we opened the
file, that someone else's problem, just keep in mind that the method
receives a file object need to return a list of dictionaries which
represent the rows in the file.

### Writing migration handler
This is where the magic happens. We going to inspect the class we
registered as a migration handler. Let's look first on the code:

```python
class AnimalMigrations(MigrationHandlerBase):

    def init_metadata(self):
        self.id = 'animal'
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
self.id = 'animal'
self.name = 'Animal migration'
self.description = 'Migrating animals into the system'
```
In this part we described the migration and what's it going to do.
Please notice that's there's an ID property. That property will help us
track which migration handler migrated which content. You should keep it
and in plural format. On the other hand... it's really that important so
you can write there any string you'ld like to(Emoji have not been tested
yet)

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
but the reference to the object.

### Alter source data
There are couple of ways to alter source data. But first - why? Well,
we can have a lot of reasons: changing a date string to a date object,
split a string into a list of other models in the DB and reference it to
the DB records which going to be inserted ino the DB. There could be
various ways:

#### Process plugins
First, let's look how to register a plugin. We'll take an example of
two plugins. In the `init_metadata` method we'll add the next section:

```python
self.fields_plugins = {
    'name': [UppercasePlugin],
    'founded_at': [{'plugin': DatePlugin, 'extra_info': {'format': '%B %d, %Y'}}]
}
```

The `fields_plugins` property is a key-value which goes by the rules
that the key is the property from the source, and the field in the DB,
and the value is a list of plugins which will take the data from the
source file and apply logic that transform it to something else.

The value is a list of referenced classes, like the `name` or maybe a
list of dictionaries which describe what's the plugin that will be
invoke, in this case the `plugin` key in the dictionary, and the
`extra_info` is a dictionary which will be passed as dictionary to the
process method in the plugin which in our case will be the format of the
string that represent a date.

Now, let's look at a plugin - the date process plugin:

```python
class DatePlugin(PluginBase):
    """
    Getting a string and transform it to a string.
    """

    def process(self, value, extra_info=None):
        return datetime.strptime(value, extra_info['format'])
```

The plugin is pretty easy to understand - the `value` argument is the
value from the source file and the `extra_info` argument represent a
list of values, such as the format date.

#### Migration life cycle hooks
TBD

## Tivol CLI commands
Let's go over some CLI commands we get out of the box:

### Migrate content
So you create content and now you to import it in? No problem. Just hit:
```bash
python manage.py migrate_content
```

You'll get something like this:
```cli
Start to migrate
 1/2 [■■■■■■■■■■■■■■--------------]  50% Animal migration: 7 migrated, 0 skipped
 2/2 [■■■■■■■■■■■■■■■■■■■■■■■■■■■■] 100% Company migration: 5 migrated, 0 skipped
Migrated
```

### Get migration information
You can get information about the migration we have in the system:

```bash
python3.6 manage.py migrations_info
```

This will return a table which look like this:

| Migration name    | Number of items   | Number of migrated items  |
| :-------------    |:-------------     | :-----                    |
| Animal migration  | 7                 | 7                         |
| Company migration | 6                 | 5                         |

### Rollback migration
There's could be a couple of reasons for rolling back the data: someone
changed the values of the migrated values and things not working
properly or just you want to clean you DB from the dummy content.

Type the next command:
```bash
python3.6 manage.py migrations_rollback
```

You'll see a nice progress bar how the procedure going:
```cli
Are you sure you want to remove any migrated data? (yes/no) [yes]
Starting to rollback migration. Collecting migrated rows
  1/13 [■■--------------------------]   7% Removing Animal:1
  2/13 [■■■■------------------------]  15% Removing Animal:2
  3/13 [■■■■■■----------------------]  23% Removing Animal:3
  4/13 [■■■■■■■■--------------------]  30% Removing Animal:4
  5/13 [■■■■■■■■■■------------------]  38% Removing Animal:5
  6/13 [■■■■■■■■■■■■----------------]  46% Removing Animal:6
  7/13 [■■■■■■■■■■■■■■■-------------]  53% Removing Animal:7
  8/13 [■■■■■■■■■■■■■■■■■-----------]  61% Removing Company:1
  9/13 [■■■■■■■■■■■■■■■■■■■---------]  69% Removing Company:2
 10/13 [■■■■■■■■■■■■■■■■■■■■■-------]  76% Removing Company:3
 11/13 [■■■■■■■■■■■■■■■■■■■■■■■-----]  84% Removing Company:4
 12/13 [■■■■■■■■■■■■■■■■■■■■■■■■■---]  92% Removing Company:5
 13/13 [■■■■■■■■■■■■■■■■■■■■■■■■■■■■] 100% Removing Company:6
```

## Extra info
If you want to look at some examples or some blog post look the next
list:
* [Dummy app](https://github.com/RoySegall/tivol-dummy-app) - holds
examples for the feature `Tivol` has to offer
