#!/usr/bin/python
"""
Class for cards list
"""
# -*- coding: utf-8 -*-

################################################################################
# Imports
################################################################################
from __future__ import print_function

from Helpers import *


################################################################################
# Cards list class
################################################################################
@singleton
class Cards(set):
    """A set where add(), remove(), and 'in' operator are thread-safe"""

    def __init__(self, *args, **kwargs):
        self._lock = RLock()
        super(self.__class__, self).__init__(*args, **kwargs)

    def add(self, elem):
        with self._lock:
            super(self.__class__, self).add(elem)

    def remove(self, elem):
        with self._lock:
            super(self.__class__, self).remove(elem)

    def __contains__(self, elem):
        with self._lock:
            return super(self.__class__, self).__contains__(elem)

    def __repr__(self):
        res = ""

        res += "#" * 10 + os.linesep
        for item in self:
            res += str(item) + os.linesep
        res += "#" * 10 + os.linesep

        return res
