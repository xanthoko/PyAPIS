DEV_INI_TEMPLATE = """[app:main]
use = egg:{{ package_name }}

[server:main]
use = egg:waitress#main
listen = localhost:6543
"""

SETUP_TEMPLATE = """from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'waitress',
]

setup(
    name='{{ package_name }}',
    install_requires=requires,
    entry_points={
        'paste.app_factory': ['main = {{ package_name }}:main'],
    },
)
"""


def get_dev_ini_str(package_name):
    return DEV_INI_TEMPLATE.replace('{{ package_name }}', package_name)


def get_setup_str(package_name):
    return SETUP_TEMPLATE.replace('{{ package_name }}', package_name)
