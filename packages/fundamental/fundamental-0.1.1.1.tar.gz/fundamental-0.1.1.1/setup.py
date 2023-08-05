from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
   name='fundamental',
   version='0.1.1.1',
   description='Dataframe downloader for fundamental financials',
   long_description=long_description,
   url= 'https://github.com/steven2K19/fundamental',
   author='Steven Wang',
   author_email='steven.wang0619@gmail.com',
   license='MIT',
   packages=find_packages(),
   install_requires=['numpy', 'pandas','yfinance','datetime', 'lxml',
                     'pandas_market_calendars','pandas.tseries.offsets']
)







