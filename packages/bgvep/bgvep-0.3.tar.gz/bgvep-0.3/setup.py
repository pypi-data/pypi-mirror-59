from os import path
from setuptools import setup, find_packages


VERSION = "0.3"
DESCRIPTION = "BBGLab tool"

directory = path.dirname(path.abspath(__file__))

# Get requirements from the requirements.txt file
with open(path.join(directory, 'requirements.txt')) as f:
    required = f.read().splitlines()


# Get the long description from the README file
with open(path.join(directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='bgvep',
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://bitbucket.org/bgframework/bgvep",
    author="Barcelona Biomedical Genomics Lab",
    author_email="bbglab@irbbarcelona.org",
    license="Apache Software License 2.0",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'bgvep = bgvep.cli:cli',
        ]
    }
)