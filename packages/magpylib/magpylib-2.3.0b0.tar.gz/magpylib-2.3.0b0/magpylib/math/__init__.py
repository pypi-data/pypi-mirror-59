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
This module includes several practical functions for working with axis-angle
relations and genmeralized rotations.
"""

__all__ = ["randomAxis", "randomAxisV", "axisFromAngles", "axisFromAnglesV",
           "anglesFromAxis", "anglesFromAxisV",
           "angleAxisRotation", "angleAxisRotationV"]  # This is for Sphinx

from magpylib._lib.mathLib import randomAxis
from magpylib._lib.mathLib import axisFromAngles
from magpylib._lib.mathLib import anglesFromAxis
from magpylib._lib.mathLib import angleAxisRotation

from magpylib._lib.mathLib_vector import randomAxisV
from magpylib._lib.mathLib_vector import axisFromAnglesV
from magpylib._lib.mathLib_vector import anglesFromAxisV
from magpylib._lib.mathLib_vector import angleAxisRotationV
