#!/usr/bin/env python
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/external/lib/python')
from clint.textui import progress

class Test:
    def __init__(self):
        self.header   = ''
        self.contents = ''

    def header_callback(self, buf):
        self.header = self.header + buf

    def body_callback(self, buf):
        self.contents = self.contents + buf

    def progress_callback(self, download_t, download_d, upload_t, upload_d):
        print 'total to upload', upload_t
        print 'total uploaded', upload_d

class FileContent(Test):

    def __init__(self, mode, fpath_local):

        # TODO: use new style constructor inheritance
        Test.__init__(self)

        self.fd = None 
        self.mode = mode
        self.content_length = 0
        self.c_transferred = 0
        self.r_transferred = 0

        self.bar = progress.Bar(label='%s ' % os.path.basename(fpath_local), expected_size=100)

        # for file upload, we use the HTTPPOST to post a form rather than reading file content 
        if self.mode == 'download':
            self.fd = open(fpath_local, 'wb')

    def header_callback(self, buf):
        self.header = self.header + buf
        re_cnt_length = re.compile(r'Content-Length:\s+([0-9]*)$')
        m = re_cnt_length.match(buf.strip())
        if m:
            self.content_length = int(m.group(1))

    def read_callback(self, size):
        return self.fd.read(size)

    def write_callback(self, buf):
        self.fd.write(buf)

    def progress_callback(self, download_t, download_d, upload_t, upload_d):

        total_size = self.content_length
        if self.mode == 'upload':
           # get total size of transfer from upload_t
            total_size = upload_t
            if upload_d != self.c_transferred:
                self.c_transferred = upload_d
        else:
            if download_d != self.c_transferred:
                self.c_transferred = download_d

        if total_size:
            r = int(100*self.c_transferred/total_size)
            if r != self.r_transferred:
                self.bar.show(r)
                self.r_transferred = r
        else:
            self.bar.show(0)

    def close(self):
        if self.fd:
            self.fd.close()
        self.bar.done()
