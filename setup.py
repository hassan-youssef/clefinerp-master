from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in clefinerp/__init__.py
from clefinerp import __version__ as version

setup(
	name='clefinerp',
	version=version,
	description='ERPNext Version Supported and Powered by ClefinCode Company ',
	author='clefincode.com',
	author_email='info@clefincode.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
