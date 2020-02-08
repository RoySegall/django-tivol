from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file.
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-tivol',
    version='0.0.1',
    description=u"Migrating (dummy) content into a Django site",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'PyYAML==5.3',
        'clikit==0.4.1',
        'requests==2.22.0',
    ],
    classifiers=[],
    keywords='',
    author=u"Roy Segall",
    author_email='roy@segall.io',
    url='https://github.com/RoySegall/tivol',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
