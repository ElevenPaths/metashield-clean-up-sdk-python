from io import open
from setuptools import setup, find_packages
from metashield_clean_up import __version__


def read_file(filepath):
    return open(filepath, 'r', encoding='utf-8').read()


EXCLUDE_FROM_PACKAGES = ['tests']


setup(
    name='metashield_clean_up',
    version=__version__,
    description='Metashield Clean-up Online API SDK',
    long_description=read_file('README.md'),
    author='Eleven Paths',
    install_requires=read_file('requirements.txt').splitlines(),
    keywords=['sdk', 'api', 'client', 'clean-up', 'metashield'],
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    zip_safe=False
)
