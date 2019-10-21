import urllib2
import os
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser, object):

    def __init__(self):
        self.intable = False
        self.incell = False
        self.inhead = False
        self.table = []
        self.header = []
        self.currow = []
        super(MyHTMLParser, self).__init__()
        
    def handle_starttag(self, tag, attrs):
        if self.intable :
            #print tag, attrs
            if tag == 'td' :
                self.incell = True
            if tag == 'th' :
                self.inhead = True
            if tag == 'tr':
                if len(self.currow)>1:
                    self.table.append(self.currow)
                    self.currow =[]
        if tag.lower()=='table':
            self.intable = True
            #print "Encountered a start tag:", tag, attrs
            
    def handle_endtag(self, tag):
        if self.intable :
            #print tag
            if tag == 'td' :
                self.incell = False
            if tag == 'th':
                self.inhead = False
            if tag == 'tr' :
                self.table.append(self.currow)
                self.currow = []
        if tag.lower()=='table':
            self.intable = False
        #print "Encountered an end tag:", tag

    def handle_data(self, data):
        if self.intable :
            #print data
            if self.incell :
                self.currow.append(data)
            if self.inhead:
                self.header.append(data)
                
        #print "Encountered some data:", data

def all_trains():
    response = urllib2.urlopen('http://trainview.septa.org/')
    content = response.read()
    #filename = 'all_trains.txt'
    #with file(filename) as f:
    #    content = f.read()
    parser = MyHTMLParser()
    parser.feed(content)
    return parser.table[1:]

def one_train(train_number):
    response = urllib2.urlopen('http://trainview.septa.org/%d' % (train_number,))
    content = response.read()
    #filename = 'train_553.txt'
    #with file(filename) as f:
    #    content = f.read()
    parser = MyHTMLParser()
    parser.feed(content)
    return parser.table[2:]

def format_table(tbl,fmt):
    s = ''
    for row in tbl:
        s += (fmt % tuple(row)) + '\n'
    return s

fmt1 = '%-24s %9s %-20s %9s'
fmt2 = '%-24s %9s %9s %9s %9s'
