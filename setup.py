from setuptools import setup, find_packages

setup(
    name = "partuniverse",
    version = "0.3",
    url = 'http://github.com/frlan/partuniverse',
    license = 'AGPLv3+',
    description = "Part Mangement",
    author = 'Frank Lanitz',
    packages = find_packages('partuniverse'),
    package_dir = {'': 'partuniverse'},
    install_requires = ['setuptools'],
)
