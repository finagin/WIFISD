#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

import thread

from Cards import Cards
from File import File
from Files import Files
from Helpers import *


################################################################################
# Class Card
################################################################################
class Card:
    def __init__(self, card_ip=None, card_essid=None):
        self.ip = card_ip
        self.essid = card_essid
        self.created_at = time.time()
        self.thread_ping = None
        self.thread_listener = None

    def start(self):
        self.ping()
        self.listener()
        print('Card ' + self.essid + ' (' + self.ip + ') - connect')

    def ping(self):
        if not self.thread_ping:
            self.thread_ping = thread.start_new(self.ping_thread, ())

    def ping_thread(self, pinged=None):
        while self.thread_ping:
            try:
                if ping(self.ip):
                    if pinged:
                        pinged(self)
                else:
                    self.disconnect()
            except socket.error:
                self.disconnect()
            time.sleep(5)

    def listener(self):
        self.thread_listener = thread.start_new(self.listener_thread, ())

    def listener_thread(self):
        files = Files()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, 5566))
        while self.thread_listener:
            message = sock.recv(1024)
            new_files = message.split('\00')
            for x in new_files:
                if x:
                    files.put(File(str(x[1:]), self))

    def disconnect(self):
        (Cards()).discard(self)
        self.thread_ping = None
        self.thread_listener = None
        print('Card ' + self.essid + ' (' + self.ip + ') - disconnect')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.ip == other.ip
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(self.ip)

    def __repr__(self):
        return self.essid
