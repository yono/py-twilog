#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import unittest
from twilog import twilog

class TestTwilogParser(unittest.TestCase):

    def setUp(self):
        self.parser = twilog.TwilogParser()
 
    def test_feed(self):
        html = open('test/twilog.html').read().decode('utf-8','ignore')
        self.parser.feed(html)
        tweets = self.parser.sentences
        self.assert_(len(tweets), 3)
        self.assert_(u'彼女がどうとか結婚がどうとか話してて俺はにこにこと笑っているしかなかった', tweets[0])
        self.assert_(u'金曜の反省を踏まえて水をがぶ飲みしている', tweets[1])
        self.assert_(u'飲みから帰宅中', tweets[2])


class TestTwilog(unittest.TestCase):

    def setUp(self):
        self.log = twilog.Twilog()

    def test_get_html(self):
        html = self.log.get_html('http://twilog.org/yono/date-100504')
        file = open('test/twilog.html').read()
        self.assert_(html, file)
    
    def test_get_url(self):
        url = self.log.get_url(user='yono')
        self.assert_(url, 'http://twilog.org/yono')

        aday_url = self.log.get_url(user='yono',aday=datetime.date(2010,1,1))
        self.assert_(url, 'http://twilog.org/yono/date-100101')

    def test_get_url_date(self):
        url_date = self.log.get_url_date(aday=datetime.date(2010,1,1))
        self.assert_(url_date, '100101')

    def test_format_date(self):
        self.assert_(self.log.format_date('0'), '00')
        self.assert_(self.log.format_date('9'), '09')
        self.assert_(self.log.format_date('10'), '10')

    def test_get_tweets(self):
        tweets = self.log.get_tweets('yono',datetime.date(2010,5,4))
        self.assert_(u'彼女がどうとか結婚がどうとか話してて俺はにこにこと笑っているしかなかった', tweets[0])
        self.assert_(u'金曜の反省を踏まえて水をがぶ飲みしている', tweets[1])
        self.assert_(u'飲みから帰宅中', tweets[2])

if __name__ == '__main__':
    unittest.main()
