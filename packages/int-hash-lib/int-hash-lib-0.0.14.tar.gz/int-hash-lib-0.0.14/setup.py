from setuptools import setup

setup(
    name='int-hash-lib',
    version='0.0.14',
    packages=['int_hash_lib', 'int_hash_lib.utils'],
    url='https://bitbucket.org/a_vento/int-hash-lib/src/master/',
    license='',
    author='MagicScore',
    author_email='',
    description='lib to hash data to int',
    install_requires=['phonenumbers<9']
)
