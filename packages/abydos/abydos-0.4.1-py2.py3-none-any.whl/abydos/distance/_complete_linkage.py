# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._complete_linkage.

Complete linkage distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._levenshtein import Levenshtein
from ._token_distance import _TokenDistance

__all__ = ['CompleteLinkage']


class CompleteLinkage(_TokenDistance):
    r"""Complete linkage distance.

    For two multisets X and Y, complete linkage distance
    :cite:`Deza:2016` is

        .. math::

            sim_{CompleteLinkage}(X, Y) =
            max_{i \in X, j \in Y} dist(X_i, Y_j)

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, metric=None, **kwargs):
        """Initialize CompleteLinkage instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants. (Defaults to Levenshtein distance)
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.


        .. versionadded:: 0.4.0

        """
        super(CompleteLinkage, self).__init__(tokenizer=tokenizer, **kwargs)
        if metric is None:
            self._metric = Levenshtein()
        else:
            self._metric = metric

    def dist_abs(self, src, tar):
        """Return the complete linkage distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            complete linkage distance

        Examples
        --------
        >>> cmp = CompleteLinkage()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        2
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        src, tar = self._get_tokens()

        max_val = float('-inf')

        for term_src in src.keys():
            for term_tar in tar.keys():
                max_val = max(
                    max_val, self._metric.dist_abs(term_src, term_tar)
                )

        return max_val

    def dist(self, src, tar):
        """Return the normalized complete linkage distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            normalized complete linkage distance

        Examples
        --------
        >>> cmp = CompleteLinkage()
        >>> cmp.dist('cat', 'hat')
        1.0
        >>> cmp.dist('Niall', 'Neil')
        1.0
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        src, tar = self._get_tokens()

        max_val = 0.0

        for term_src in src.keys():
            for term_tar in tar.keys():
                max_val = max(max_val, self._metric.dist(term_src, term_tar))

        return max_val


if __name__ == '__main__':
    import doctest

    doctest.testmod()
