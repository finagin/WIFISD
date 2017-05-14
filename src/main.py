#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

from Downloader import Downloader
from Helpers import *
from Scanner import Scanner


def opt():
    return [
        {
            'short': "-d",
            'long': "--dir",
            'action': None,
            'dest': "dir",
            'help': "directory for storing images",
            'default': None
        },
        {
            'short': "-i",
            'long': "--ip",
            'action': None,
            'dest': "ip",
            'help': "ip address of the computer (default %s)" % (self_ip()),
            'default': self_ip()
        },
        {
            'short': "-c",
            'long': "--card_ip",
            'action': None,
            'dest': "card_ip",
            'help': "Preset SD card IP",
            'default': None
        },
        {
            'short': "-s",
            'long': "--separate",
            'action': "store_true",
            'dest': "separate",
            'help': "Separate download folders",
            'default': False
        },
    ]


if __name__ == '__main__':
    from optparse import OptionParser

    options = opt()

    parser = OptionParser()
    for option in options:
        parser.add_option(option['short'],
                          option['long'],
                          action=option['action'],
                          dest=option['dest'],
                          default=option['default'],
                          help=option['help'])

    (options, args) = parser.parse_args()

    Scanner(station_ip=options.ip, only=options.card_ip)
    Downloader(directory=options.dir, separate=options.separate)

    while True:
        time.sleep(5)
