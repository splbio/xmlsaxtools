#!/usr/bin/env python

import sys
import os
import xml.sax
import urllib
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesNSImpl

class XMLCounter(xml.sax.ContentHandler):
    def __init__(self, verbose=False, path=None, stream=sys.stdin):
        self._stream = stream
        self._path = path
        self._stack_cmp = path.split('/')
        self._stack_cmp.pop(0)
        self._stack = []
        self._match_count = 0
        self._verbose = verbose
        self._all_count = 0

    def count(self):
        return self._match_count

    def run(self):
        xml.sax.parse(self._stream, self)
        if self._verbose and self._all_count > 10000:
            sys.stderr.write("\n")

    def startElement(self, name, attrs):
        self._stack.append(name)
        self._all_count += 1
        if self._stack_cmp == self._stack:
            self._match_count+=1
        if self._verbose and self._all_count % 10000 == 0:
            sys.stderr.write("total records: %d, matched: %d\r" % (self._all_count, self._match_count))

    def endElement(self, name):
        self._stack.pop()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='SAX get count of elements.')
    parser.add_argument('--input', help="input file")
    parser.add_argument('--path', required=True, help="xml path to count, example (/threats/ips/ip)")
    parser.add_argument('--verbose', action='store_true', help="output some progress while processing")
    args = parser.parse_args()

    if args.input:
        infile = open(args.input, 'r')
    else:
        infile = sys.stdin
    counter = XMLCounter(path = args.path, stream=infile, verbose=args.verbose)
    counter.run()
    print counter.count()
