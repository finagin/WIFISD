#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

import thread

from Card import Card
from Cards import Cards
from Helpers import *


################################################################################
# Scanner class
################################################################################
class Scanner:
    def __init__(self, station_ip=None, only=None):
        self.station_ip = self_ip() if not station_ip else station_ip
        self.only = only
        thread.start_new_thread(self.scanning, ())

    @staticmethod
    def socket():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        return sock

    def has_ip(self, sock):
        resp = sock.recv(400)
        sock.close()
        try:
            ip = resp.split('ip=')[1].split('\n')[0]
            essid = resp.split('essid=')[1].split('\n')[0]
            if is_ip(ip):
                if self.only and ip != self.only:
                    raise socket.timeout
                cards = Cards()
                new_card = Card(ip, essid)
                if new_card not in cards:
                    cards.add(new_card)
                    new_card.start()
        except IndexError:
            pass

    def scanning(self):
        while True:
            s = self.socket()
            try:
                s.bind((self.station_ip, 58255))
            except socket.error:
                s.close()
                time.sleep(1)
                continue

            s.sendto('', ('<broadcast>', 55777))

            try:
                self.has_ip(s)
            except socket.timeout:
                print('Silence..')
            finally:
                time.sleep(2)
