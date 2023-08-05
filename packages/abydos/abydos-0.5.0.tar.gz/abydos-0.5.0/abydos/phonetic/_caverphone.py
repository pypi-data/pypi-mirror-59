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

"""abydos.phonetic._caverphone.

Caverphone phonetic algorithm
"""

from deprecation import deprecated

from ._phonetic import _Phonetic
from .. import __version__

__all__ = ['Caverphone', 'caverphone']


class Caverphone(_Phonetic):
    """Caverphone.

    A description of version 1 of the algorithm can be found in
    :cite:`Hood:2002`.

    A description of version 2 of the algorithm can be found in
    :cite:`Hood:2004`.

    .. versionadded:: 0.3.6
    """

    def __init__(self, version=2):
        """Initialize Caverphone instance.

        Parameters
        ----------
        version : int
            The version of Caverphone to employ for encoding (defaults to 2)


        .. versionadded:: 0.4.0

        """
        self._version = version

    def encode_alpha(self, word):
        """Return the alphabetic Caverphone code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The alphabetic Caverphone value

        Examples
        --------
        >>> pe = Caverphone()
        >>> pe.encode_alpha('Christopher')
        'KRSTFA'
        >>> pe.encode_alpha('Niall')
        'NA'
        >>> pe.encode_alpha('Smith')
        'SMT'
        >>> pe.encode_alpha('Schmidt')
        'SKMT'

        >>> pe_1 = Caverphone(version=1)
        >>> pe_1.encode_alpha('Christopher')
        'KRSTF'
        >>> pe_1.encode_alpha('Niall')
        'N'
        >>> pe_1.encode_alpha('Smith')
        'SMT'
        >>> pe_1.encode_alpha('Schmidt')
        'SKMT'


        .. versionadded:: 0.4.0

        """
        return self.encode(word).rstrip('1')

    def encode(self, word):
        """Return the Caverphone code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Caverphone value

        Examples
        --------
        >>> pe = Caverphone()
        >>> pe.encode('Christopher')
        'KRSTFA1111'
        >>> pe.encode('Niall')
        'NA11111111'
        >>> pe.encode('Smith')
        'SMT1111111'
        >>> pe.encode('Schmidt')
        'SKMT111111'

        >>> pe_1 = Caverphone(version=1)
        >>> pe_1.encode('Christopher')
        'KRSTF1'
        >>> pe_1.encode('Niall')
        'N11111'
        >>> pe_1.encode('Smith')
        'SMT111'
        >>> pe_1.encode('Schmidt')
        'SKMT11'


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        word = word.lower()
        word = ''.join(c for c in word if c in self._lc_set)

        def _squeeze_replace(word, char):
            """Convert strings of char in word to one instance.

            Parameters
            ----------
            word : str
                The partially converted word
            char : str
                A character to 'squeeze'

            Returns
            -------
            str
                The word with instances of char squeezed down to one

            .. versionadded:: 0.1.0

            """
            while char * 2 in word:
                word = word.replace(char * 2, char)
            return word.replace(char, char.upper())

        # the main replacement algorithm
        if self._version != 1 and word[-1:] == 'e':
            word = word[:-1]
        if word:
            if word[:5] == 'cough':
                word = 'cou2f' + word[5:]
            if word[:5] == 'rough':
                word = 'rou2f' + word[5:]
            if word[:5] == 'tough':
                word = 'tou2f' + word[5:]
            if word[:6] == 'enough':
                word = 'enou2f' + word[6:]
            if self._version != 1 and word[:6] == 'trough':
                word = 'trou2f' + word[6:]
            if word[:2] == 'gn':
                word = '2n' + word[2:]
            if word[-2:] == 'mb':
                word = word[:-1] + '2'
            for src, tar in (
                ('cq', '2q'),
                ('ci', 'si'),
                ('ce', 'se'),
                ('cy', 'sy'),
                ('tch', '2ch'),
                ('c', 'k'),
                ('q', 'k'),
                ('x', 'k'),
                ('v', 'f'),
                ('dg', '2g'),
                ('tio', 'sio'),
                ('tia', 'sia'),
                ('d', 't'),
                ('ph', 'fh'),
                ('b', 'p'),
                ('sh', 's2'),
                ('z', 's'),
            ):
                word = word.replace(src, tar)
            if word[0] in self._lc_v_set:
                word = 'A' + word[1:]
            for vowel in 'aeiou':
                word = word.replace(vowel, '3')
            if self._version != 1:
                word = word.replace('j', 'y')
                if word[:2] == 'y3':
                    word = 'Y3' + word[2:]
                if word[:1] == 'y':
                    word = 'A' + word[1:]
                word = word.replace('y', '3')
            for src, tar in (('3gh3', '3kh3'), ('gh', '22'), ('g', 'k')):
                word = word.replace(src, tar)

            for char in 'stpkfmn':
                word = _squeeze_replace(word, char)

            word = word.replace('w3', 'W3')
            if self._version == 1:
                word = word.replace('wy', 'Wy')
            word = word.replace('wh3', 'Wh3')
            if self._version == 1:
                word = word.replace('why', 'Why')
            if self._version != 1 and word[-1:] == 'w':
                word = word[:-1] + '3'
            word = word.replace('w', '2')
            if word[:1] == 'h':
                word = 'A' + word[1:]
            word = word.replace('h', '2')
            word = word.replace('r3', 'R3')
            if self._version == 1:
                word = word.replace('ry', 'Ry')
            if self._version != 1 and word[-1:] == 'r':
                word = word[:-1] + '3'
            word = word.replace('r', '2')
            word = word.replace('l3', 'L3')
            if self._version == 1:
                word = word.replace('ly', 'Ly')
            if self._version != 1 and word[-1:] == 'l':
                word = word[:-1] + '3'
            word = word.replace('l', '2')
            if self._version == 1:
                word = word.replace('j', 'y')
                word = word.replace('y3', 'Y3')
                word = word.replace('y', '2')
            word = word.replace('2', '')
            if self._version != 1 and word[-1:] == '3':
                word = word[:-1] + 'A'
            word = word.replace('3', '')

        # pad with 1s, then extract the necessary length of code
        word += '1' * 10
        if self._version != 1:
            word = word[:10]
        else:
            word = word[:6]

        return word


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Caverphone.encode method instead.',
)
def caverphone(word, version=2):
    """Return the Caverphone code for a word.

    This is a wrapper for :py:meth:`Caverphone.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    version : int
        The version of Caverphone to employ for encoding (defaults to 2)

    Returns
    -------
    str
        The Caverphone value

    Examples
    --------
    >>> caverphone('Christopher')
    'KRSTFA1111'
    >>> caverphone('Niall')
    'NA11111111'
    >>> caverphone('Smith')
    'SMT1111111'
    >>> caverphone('Schmidt')
    'SKMT111111'

    >>> caverphone('Christopher', 1)
    'KRSTF1'
    >>> caverphone('Niall', 1)
    'N11111'
    >>> caverphone('Smith', 1)
    'SMT111'
    >>> caverphone('Schmidt', 1)
    'SKMT11'

    .. versionadded:: 0.1.0

    """
    return Caverphone(version).encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
