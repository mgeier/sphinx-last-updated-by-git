from pathlib import Path

from setuptools import setup


# "import" __version__
__version__ = 'unknown'
with Path('src/sphinx_last_updated_by_git.py').open() as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line)
            break

setup(
    name='sphinx-last-updated-by-git',
    version=__version__,
    package_dir={'': 'src'},
    py_modules=['sphinx_last_updated_by_git'],
    python_requires='>=3.7',
    install_requires=[
        'sphinx>=1.8',
    ],
    author='Matthias Geier',
    author_email='Matthias.Geier@gmail.com',
    description='Get the "last updated" time for each Sphinx page from Git',
    long_description=Path('README.rst').read_text(),
    license='BSD-2-Clause',
    keywords='Sphinx Git'.split(),
    url='https://github.com/mgeier/sphinx-last-updated-by-git/',
    platforms='any',
    classifiers=[
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx',
    ],
    zip_safe=True,
)
