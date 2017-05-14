#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function


################################################################################
# Class File
################################################################################
class File:
    def __init__(self, file_name, file_from=None):
        self.file_name = file_name
        self.file_from = file_from

    def get_name(self):
        return self.file_name.split('/')[-1]

    def get_path(self):
        return self.file_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(self.file_name + str(self.file_from.__hash__()))

    def __repr__(self):
        return self.file_name + (' from ' + str(self.file_from) if self.file_from else '')
