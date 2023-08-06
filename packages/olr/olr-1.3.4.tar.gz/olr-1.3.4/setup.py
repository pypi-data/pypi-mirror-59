import os
import setuptools
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name="olr",
    version="1.3.4",
    author="Mathew Fok",
    author_email="mfok@stevens.edu",
    description="olr: Optimal Linear Regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/MatHatter",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'numpy'],
    data_files= [('Lib\site-packages\olr', ['data\oildata.csv'])],
    py_modules=['__init__', 'olr_function'],
    classifers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
)


