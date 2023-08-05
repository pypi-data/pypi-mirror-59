# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['bacchus']

package_data = \
{'': ['*'], 'bacchus': ['templates/*']}

install_requires = \
['cleo>=0.7.6,<0.8.0', 'docker>=4.1,<5.0']

entry_points = \
{'console_scripts': ['bacchus = bacchus.cli:main']}

setup_kwargs = {
    'name': 'bacchus',
    'version': '0.1.1',
    'description': 'Home Server solution based on docker',
    'long_description': None,
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
