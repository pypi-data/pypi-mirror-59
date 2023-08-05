import setuptools
from setuptools import setup

with open('README.md', 'r') as in_file:
    long_description = in_file.read()

setup(
    name="pymensor",
    version="0.0.1",
    description="Python driver for Mensor Modular Pressure Controllers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/stevenlowery011/pymensor.git",
    author="Steven Lowery",
    author_email="steven.lowery011@gmail.com",
    packages=["pymensor"],
    install_requires=["pyvisa"],
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ]
)
