#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

from Downloader import Downloader
from Helpers import *
from Scanner import Scanner
from Storage import Storage


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
            'default': None
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
        {
            'short': "-t",
            'long': "--threads",
            'action': None,
            'dest': "threads",
            'help': "Count of threads",
            'default': 4
        },
        {
            'short': "-D",
            'long': "--not-download-old",
            'action': "store_true",
            'dest': "not_download_old",
            'help': "Not download old photos",
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
    Storage(directory=options.dir, not_download_old=options.not_download_old)
    Downloader(separate=options.separate, thread_count=options.threads)

    while True:
        time.sleep(10)
