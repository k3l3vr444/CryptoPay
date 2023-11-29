from setuptools import setup

setup(
    name='crypto_pay',
    version='0.1',
    description='https://help.crypt.bot/crypto-pay-api API wrapper',
    author='k3l3vr444',
    author_email='ayukanov.nikita@gmail.com',
    packages=['crypto_pay'],  # same as name
    install_requires=['aiohttp'],  # external packages as dependencies
)
