#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

import thread
import urllib

from Files import Files
from Helpers import *


################################################################################
# Downloader class
################################################################################
class Downloader:
    def __init__(self, directory=None, separate=False, folder='WIFISD'):
        self.dir = directory if directory else os.path.expanduser('~')
        self.separate = separate

        if not os.path.exists(os.path.join(self.dir, folder)):
            os.mkdir(os.path.join(self.dir, folder))
        self.dir = os.path.join(self.dir, folder)

        thread.start_new_thread(self.downloading, ())

    def downloading(self, download_callback=None, download_complete=None):
        files = Files()

        while True:
            if not files.empty():
                download_file = files.get()
                download_from_ip = download_file.file_from.ip
                download_from_card = download_file.file_from.essid

                download_url = 'http://%s/cgi-bin/wifi_download?fn=%s' % (download_from_ip, download_file.get_path())
                download_to = self.dir
                if self.separate:
                    download_to = os.path.join(download_to, download_from_card)
                    if not os.path.exists(download_to):
                        os.mkdir(download_to)
                download_to = os.path.join(download_to, download_file.get_name())

                urllib.urlretrieve(download_url, download_to, download_callback)

                if download_complete:
                    download_complete(download_to)

            time.sleep(0.1)
