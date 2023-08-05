# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dit_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['dit = dit_cli.dit:cli']}

setup_kwargs = {
    'name': 'dit-cli',
    'version': '0.1.0',
    'description': 'The CLI for dit',
    'long_description': 'This is the CLI for dit. Dit is a type of arbitrary container file. This CLI can interact with scripts in dit files, like telling them to validate themselves. See more at [DitaBase.io](https://www.ditabase.io/)\n',
    'author': 'Isaiah Shiner',
    'author_email': 'shiner.isaiah@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.ditabase.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
