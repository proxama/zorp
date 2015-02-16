from setuptools import setup

with open("README.txt") as readme:
    long_description = readme.read()

setup(
    name='zorp',
    packages=['zorp'],
    version='0.1.1',
    author='Steve Engledow',
    author_email='steve.engledow@proxama.com',
    url='https://git.prx.ma/server/zorp.git',
    description='A ZeroMQ RPC library',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
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
    install_requires=['pyzmq', 'jsonschema', 'pymongo'],
)
