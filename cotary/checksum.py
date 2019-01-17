# Copyright (C) 2019 Wanja Chresta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib

class Checksum(object):
    """Calculate and represent a checksum of a file."""

    def __init__(self, iterator):
        """
        Create a new checksum from the given string, file-handle or iterator.
        Make sure a file is opened in binary mode!
        """

        self.hash_function = hashlib.sha256
        self.hash_name = self.hash_function.__name__
        self.checksum = self.calc_checksum(iterator)

        if self.checksum is None:
            raise ValueError("Empty checksum")

    def calc_checksum(self, iterator):
        """
        Calculate the sha256 checksum piecewise from iterator and 
        return a hex representation.

        If input is empty, return None
        """

        checksum = self.hash_function()
        empty = True
        for part in iterator:
            checksum.update(part)
            empty = False

        if empty:
            return None

        checksum_hex = checksum.hexdigest()
        return checksum_hex

    def __str__(self):
        return "{}:{}".format(self.hash_name, self.checksum)

if __name__=="__main__":
    print(Checksum(iter([b"Hello",b" World!"])))

