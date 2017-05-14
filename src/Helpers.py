#!/usr/bin/python
"""Helpers for information retrieval"""
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

import os
import re
import socket
import time
from Queue import Queue as BaseQueue
from threading import RLock

################################################################################
# Print thread safe
################################################################################
_print = print
_rlock = RLock()
_time = time.time()
_iter = 0


def print(*args, **kwargs):
    global _iter
    with _rlock:
        _iter += 1
        __time = round((time.time() - _time) * 100)
        __tlen = len(str(__time))
        __time = str(__time / 100)
        while len(__time) < __tlen or len(__time) < 5:
            __time += '0'
        __iter = str(_iter)
        prefix = '[ '
        while len(prefix + __iter) < 0x6:
            prefix += ' '
        prefix += __iter
        prefix += ' | '
        while len(prefix + __time) < 0x12:
            prefix += ' '
        prefix += __time
        prefix += ' ] '
        _print(prefix, *args, **kwargs)


################################################################################
# Singleton
################################################################################
def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


################################################################################
# Class queue like set
################################################################################
class Queue(BaseQueue):
    def _init(self, maxsize=0):
        self.queue = set()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

    def clear(self):
        while len(self.queue) > 0:
            self.queue.pop()


################################################################################
# Check valid ip
################################################################################
def is_ip(ip):
    return [0 <= int(x) < 256 for x in re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', ip).group(0))].count(True) == 4


################################################################################
# Self station ip
################################################################################
def self_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception, e:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


################################################################################
# Write to output file
################################################################################
def output(string, add=False, file_name="./output.txt"):
    f = open(file_name, 'a+')
    if add:
        f.writelines(str(string) + os.linesep)
    else:
        f.write(str(string))
    f.close()


################################################################################
# Ping implements
################################################################################
def ping(host):
    """
    Returns True if host responds to a ping request
    """
    import platform
    import subprocess

    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if platform.system().lower() == "windows" else True

    return subprocess.call(args, shell=need_sh, stdout=open(os.devnull, 'w')) == 0
