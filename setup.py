"""
Setup script for treedir package.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="treedir",
    version="0.1.0",
    author="Parth Nuwal",
    author_email="parthnuwal7@gmail.com",
    description="A Python library for parsing directory structures from text files and implementing them in target folders",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Parthnuwal7/treedir",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    keywords="directory structure tree filesystem automation",
    project_urls={
        "Bug Reports": "https://github.com/Parthnuwal7/treedir"
    },
    entry_points={
        'console_scripts': [
            'treedir=treedir.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)