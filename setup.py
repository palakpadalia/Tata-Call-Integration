from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tata_app/__init__.py
from tata_app import __version__ as version

setup(
	name="tata_app",
	version=version,
	description="Tata App",
	author="Srushti Shah",
	author_email="srushti@sanskartechnolab.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
