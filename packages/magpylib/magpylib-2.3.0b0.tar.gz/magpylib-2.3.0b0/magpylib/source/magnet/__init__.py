# -------------------------------------------------------------------------------
# magpylib -- A Python 3 toolbox for working with magnetic fields.
# Copyright (C) Silicon Austria Labs, https://silicon-austria-labs.com/,
#               Michael Ortner <magpylib@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/>.
# The acceptance of the conditions of the GNU Affero General Public License are
# compulsory for the usage of the software.
#
# For contact information, reach out over at <magpylib@gmail.com> or our issues
# page at https://www.github.com/magpylib/magpylib/issues.
# -------------------------------------------------------------------------------
"""
This subpackage provides the permanent magnet classes that are used for field 
computation. They include `Box` (cuboid shape), `Cylinder` (cylindrical shape)
`Sphere` (spherical shape) and `Facet` (triangular surface of magnet body). 
"""

__all__ = ["Box", "Cylinder", "Sphere", "Facet"]  # This is for Sphinx

from magpylib._lib.classes.magnets import Box
from magpylib._lib.classes.magnets import Cylinder
from magpylib._lib.classes.magnets import Sphere
from magpylib._lib.classes.magnets import Facet