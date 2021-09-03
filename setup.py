"""Setup file for the bot"""
from setuptools import setup

setup(
    name='Winterburn starcraft2 bot',
    version='0.1',
    description='Bot that plays starcraft 2',
    author='Winterburn',
    packages=['bot'],
    install_requires=[
        'burnysc2',
    ]
)
