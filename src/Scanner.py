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
        self.static_station_ip = station_ip
        self.station_ip = self.get_self_ip if not station_ip else self.get_station_ip
        self.only = only
        thread.start_new_thread(self.scanning, ())

    @staticmethod
    def socket():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        return sock

    def get_station_ip(self):
        return self.static_station_ip

    @staticmethod
    def get_self_ip():
        return self_ip()

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
        sleep_time = 5
        while True:
            s = self.socket()
            try:
                s.bind((self.station_ip(), 58255))
            except socket.error:
                s.close()
                print('Silence...')
                time.sleep(sleep_time)
                continue

            try:
                s.sendto('', ('<broadcast>', 55777))
                self.has_ip(s)
            except socket.timeout:
                print('Silence..')
            finally:
                s.close()
                time.sleep(sleep_time)
