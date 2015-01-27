from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zorp',
    version='0.1.0',
    description='A ZeroMQ RPC library',
    long_description=long_description,
    url='https://git.prx.ma/steve.engledow/zorp.git',
    author='Steve Engledow',
    author_email='steve.engledow@proxama.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='development zeromq rpc',
    packages=find_packages(exclude=['tests*']),
    install_requires=['pyzmq', 'jsonschema', 'pymongo'],
)
