from setuptools import setup, find_packages
import os

setup(
    name = 'ezsql',
    version = '0.1.0',
    description = 'Help you maintain a complex SQL script',
    license = 'MIT License',
    url = 'https://github.com/uudoublek/ezsql',
    author = 'uudoublek',
    author_email = 'uu_double_k@163.com',
    packages = find_packages(),
    include_package_data = False,
    platforms = 'any',
    entry_points = {
        'console_scripts': [
            'ezsql=ezsql.main:main'
        ],
    }
)