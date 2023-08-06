"""A setuptools based setup module for Grapetree.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path, walk

__licence__ = 'GPLv3'
__author__ = 'EnteroBase development team'
__author_email__ = 'zhemin.zhou@warwick.ac.uk'
__version__ = '2.1'

def package_files(directory):
    paths = []
    for (pathz, directories, filenames) in walk(directory):
        for filename in filenames:
            paths.append(path.join('..', pathz, filename))
    return paths

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def recursive(folder) :
    return [path.join(p, fn) for (p, directories, filenames) in walk('static') for fn in filenames ]


setup(
    name='grapetree',
    version= __version__,
    description='Web interface of GrapeTree, which is a program for phylogenetic analysis.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/achtman-lab/GrapeTree',
    author= __author__,
    author_email= __author_email__,
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
	entry_points={
        'console_scripts': [
            'grapetree = grapetree.grapetree:main',
        ],
    },
    keywords=['bioinformatics', 'microbial', 'genomics', 'MLST', 'visulisation'],
    package_data={'grapetree':[
        'MSTree_holder.html',
        'GT_icon*',
        'README*',
        'LICENSE',
        'module/*',
        'binaries/*',
    ]+recursive('static')},
    packages = ['grapetree'],
    package_dir = {'grapetree':'.'},
    install_requires=['ete3', 'numpy', 'Flask', 'networkx', 'psutil', 'numba'],
    include_package_data=True,
    project_urls={
        'Bug Reports': 'https://github.com/achtman-lab/GrapeTree/issues',
        'Source': 'https://github.com/achtman-lab/GrapeTree',
    },
)
