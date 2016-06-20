from setuptools import setup, find_packages

setup(
    name = "partuniverse",
    version = "1.0",
    url = 'http://github.com/frlan/partuniverse',
    license = 'BSD',
    description = "Part Mangement",
    author = 'Frank Lanitz',
    packages = find_packages('partuniverse'),
    package_dir = {'': 'partuniverse'},
    install_requires = ['setuptools'],
)
