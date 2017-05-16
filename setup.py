import io
import os
import re
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


def read(*names, **kwargs):
    with io.open(
        os.path.join(here, *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def readme():
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()


setup(
    name='Stoichiograph',
    version=find_version('stoichiograph', '__init__.py'),
    description=(
        'Spell words with elemental symbols from the periodic table ("He", "Cu", etc).'
    ),
    long_description=readme(),
    url='https://github.com/mesbahamin/stoichiograph',
    author='Amin Mesbah',
    author_email='mesbahamin@gmail.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='command-line chemistry words fun combinatorics spelling',
    packages=['stoichiograph'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'stoichiograph = stoichiograph.stoichiograph:main',
        ],
    },
)
