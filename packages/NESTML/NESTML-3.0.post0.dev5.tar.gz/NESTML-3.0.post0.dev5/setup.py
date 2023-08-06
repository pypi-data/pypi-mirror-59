#
# setup.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import sys

assert sys.version_info.major >= 3, "Python 3 is required to run PyNESTML"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='NESTML',
    version='3.0-post-dev5',
    description='NESTML is a domain specific language that supports the specification of neuron models in a'
                ' precise and concise syntax, based on the syntax of Python. Model equations can either be given'
                ' as a simple string of mathematical notation or as an algorithm written in the built-in procedural'
                ' language. The equations are analyzed by NESTML to compute an exact solution if possible or use an '
                ' appropriate numeric solver otherwise.',
    license='GNU General Public License v2.0',
    url='https://github.com/nest/nestml',
    packages=find_packages(),
     package_data={'pynestml': ['codegeneration/resources_nest/*.jinja2',
                                'codegeneration/resources_nest/setup/*.jinja2',
                                'codegeneration/resources_nest/directives/*.jinja2']},
    entry_points = {
        'console_scripts': [
            'nestml = pynestml.frontend.pynestml_frontend:main',
        ],
    },

    install_requires=requirements,
    test_suite='tests',
)

