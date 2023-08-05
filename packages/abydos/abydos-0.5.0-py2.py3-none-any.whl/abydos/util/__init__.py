# Copyright 2014-2020 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.util.

The util module defines various utility functions for other modules within
Abydos, including:

    - _prod -- computes the product of a collection of numbers (akin to sum)

These functions are not intended for use by users.
"""

from ._data import (
    data_path,
    download_package,
    list_available_packages,
    list_installed_packages,
    package_path,
)

__all__ = [
    'data_path',
    'download_package',
    'list_available_packages',
    'list_installed_packages',
    'package_path',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
