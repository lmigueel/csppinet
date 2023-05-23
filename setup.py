#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   This file is part of the tspex package, available at:
#   https://github.com/lmigueel/csppinet
#
#   Tspex is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#   Contact: lucasmigueel@gmail.com

"""The setup script."""

from setuptools import setup, find_packages

setup(
    name='csppinet',
    version='1.0',
    packages=find_packages(),
    license='GNU General Public License v3.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description='A Python package for context-specific protein-protein interaction network construction and analysis based on omics data.',
    install_requires=[ 'numpy', 'pandas', 'networkx >= 2.5'],
    python_requires='>=3',
    entry_points={
        'console_scripts': ['csppinet=csppinet.csppinet:main'],
    },
    url='https://github.com/lmigueel/csppinet/',
    keywords=['bioinformatics', 'context-specific network','PPI network', 'interactome','network analysis','omics'],
    author='Luca Miguel de Carvalho',
    author_email='lucasmigueel@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
    ],
)
