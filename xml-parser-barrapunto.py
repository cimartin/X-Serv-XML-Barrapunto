#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib import request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.line = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                # To avoid Unicode trouble
                self.line = "Title: " + self.theContent + "."
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                lnk = "<li><a href='" + self.theContent + "'>" + self.line + "</a></li><br/>"
                print (lnk)
                self.inContent = False
                self.theContent = ""
                self.line = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

print("<!DOCTYPE html><html><body>")
print("<ul>")

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)


url = "http://barrapunto.com/index.rss"
xmlStream = request.urlopen(url)
theParser.parse(xmlStream)
print("</ul></body></html>")
