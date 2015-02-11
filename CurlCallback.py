#!/usr/bin/env python

class Test:
    def __init__(self):
        self.header   = ''
        self.contents = ''

    def header_callback(self, buf):
        self.header = self.header + buf

    def body_callback(self, buf):
        self.contents = self.contents + buf
