#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
# Imports
################################################################################
from __future__ import print_function

import thread
import urllib

from File import File
from Files import Files
from Helpers import *
from Storage import Storage


################################################################################
# Downloader class
################################################################################
class Downloader:
    def __init__(self, separate=False, thread_count=4):
        self.separate = separate

        for iteration in range(thread_count):
            thread.start_new_thread(self.downloading, ())

    def downloading(self, download_callback=None, download_complete=print):
        files = Files()

        while True:
            if not files.empty():
                download_file = files.get()
                download_from_ip = download_file.file_from.ip
                download_from_card = download_file.file_from.essid

                download_url = 'http://%s/cgi-bin/wifi_download?fn=%s' % (download_from_ip, download_file.get_path())
                download_to = Storage().dir()
                if self.separate:
                    download_to = os.path.join(download_to, download_from_card)
                    if not os.path.exists(download_to):
                        os.mkdir(download_to)
                download_to = os.path.join(download_to, download_file.get_name())

                try:
                    urllib.urlretrieve(download_url, download_to, download_callback)

                    Storage().add(File(download_file.get_name()))

                    if download_complete:
                        download_complete(download_to)
                except urllib.ContentTooShortError:
                    print('Oops!!')

            time.sleep(0.1)
