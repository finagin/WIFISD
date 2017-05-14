#!/usr/bin/python
"""
Class for files list
"""
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

from Helpers import *


################################################################################
# Class Files
################################################################################
@singleton
class Files(Queue):
    def __repr__(self):
        res = ""

        res += "#" * 10 + os.linesep
        for item in self.queue:
            res += str(item) + os.linesep
        res += "#" * 10 + os.linesep

        return res
