#!/usr/bin/python
"""
Class for cards list
"""
# -*- coding: utf-8 -*-

################################################################################
# Imports
################################################################################
from __future__ import print_function

from File import File
from Helpers import *


################################################################################
# Cards list class
################################################################################
@singleton
class Storage(set):
    """A set where add(), remove(), and 'in' operator are thread-safe"""

    def __init__(self, directory=None, folder='WIFISD', not_download_old=False, *args, **kwargs):
        self._lock = RLock()
        self._dir = directory if directory else os.path.expanduser('~')

        if not os.path.exists(os.path.join(self._dir, folder)):
            os.mkdir(os.path.join(self._dir, folder))
        self._dir = os.path.join(self._dir, folder)

        super(self.__class__, self).__init__(*args, **kwargs)

        if not not_download_old:
            self.add_locals()

    def dir(self):
        return self._dir

    def add_locals(self):
        for file_name in os.listdir(self._dir):
            self.add(File(file_name))

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
        res = os.linesep

        res += "#" * 10 + os.linesep
        for item in self:
            res += str(item) + os.linesep
        res += "#" * 10 + os.linesep

        return res
