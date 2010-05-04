#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from HTMLParser import HTMLParser
import time
import urllib2
import urlparse

class Twilog(object):

    BASEURL = "http://twilog.org/"

    def __init__(self):
        self.parser = TwilogParser()

    def get_html(self, url):
        time.sleep(5)
        fp = urllib2.urlopen(url)
        html = unicode(fp.read(),'utf-8','ignore')
        return html

    def get_url(self, user, aday=''):
        url = self.BASEURL+user
        if aday:
            return url+'/date-'+self.get_url_date(aday)
        else:
            return url

    def get_tweets(self, user, aday=''):
        url = self.get_url(user, aday)
        html = self.get_html(url)
        self.parser.sentences = []
        self.parser.feed(html)
        tweets = self.parser.sentences
        return tweets

    def get_url_date(self, aday):
        year = str(aday.year)[2:4]
        month = self.format_date(str(aday.month))
        day = self.format_date(str(aday.day))
        return "%s%s%s" % (year, month, day)

    def format_date(self, date):
        return date if len(date) == 2 else "0%s" % (date)


class TwilogParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.words = []
        self.sentences = []
    
    def handle_starttag(self, tag, attrs):
        attrs_dic = dict(attrs)

        if tag == 'p' and 'class' in attrs_dic:
            if attrs_dic['class'] == 'tl-text':
                self.flag = True

    def handle_data(self, data):
        if self.flag:
            self.words.append(data)

    def handle_endtag(self, tag):
        if tag == 'p':
            sentence = ''.join(self.words)
            if sentence != '':
                self.sentences.append(sentence)
            self.words = []
            self.flag = False

if __name__ == '__main__':
    log = Twilog()
    tweets = log.get_tweets('yono')
    for tweet in tweets:
        print tweet

    print '------ Today\'s Tweets ------'

    tweets = log.get_tweets('yono',datetime.date.today())
    for tweet in tweets:
        print tweet

