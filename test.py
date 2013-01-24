#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import unittest
from twilog import twilog


class TestTwilogParser(unittest.TestCase):

    def setUp(self):
        self.parser = twilog.TwilogParser()

    def test_feed(self):
        html = open('test/twilog.html').read().decode('utf-8', 'ignore')
        self.parser.feed(html)
        tweets = self.parser.sentences
        end_tweets = [
            u'ウィッシュリストが増えていくが減る見込みがない',
            u'旅立つのは明日にしようかやっぱ',
            u'ちょっと旅立ってくる',
            u'休み長いから使わずに置いといてどっかで使いたい',
            u'スパ4買おうかなぁ',
            u'彼女がどうとか結婚がどうとか話してて俺はにこにこと笑っている\
                    しかなかった',
            u'金曜の反省を踏まえて水をがぶ飲みしている',
            u'飲みから帰宅中',
        ]
        self.assert_(len(tweets), len(end_tweets))
        for i in xrange(len(tweets)):
            self.assert_(tweets[i], end_tweets[i])


class TestTwilog(unittest.TestCase):

    def setUp(self):
        self.log = twilog.Twilog()

    def test_to_html(self):
        html = self.log._Twilog__to_html('http://twilog.org/yono/date-100504')
        file = open('test/twilog.html').read()
        self.assert_(html, file)

    def test_to_url(self):
        url = self.log._Twilog__to_url(user='yono')
        self.assert_(url, 'http://twilog.org/yono')

        aday_url = self.log._Twilog__to_url(user='yono',
                                    aday=datetime.date(2010, 1, 1))
        self.assert_(url, 'http://twilog.org/yono/date-100101')

    def test_to_url_date(self):
        url_date = self.log._Twilog__to_url_date(aday=datetime.date(2010, 1, 1))
        self.assert_(url_date, '100101')

    def test_format_date(self):
        self.assert_(self.log._Twilog__format_date('0'), '00')
        self.assert_(self.log._Twilog__format_date('9'), '09')
        self.assert_(self.log._Twilog__format_date('10'), '10')

    def test_get_tweets(self):
        start = datetime.date(2010, 5, 3)
        end = datetime.date(2010, 5, 4)

        start_tweets = [
            u'ついったーの話とか出たけどスルー',
            u'何もかも知らないふりしてる',
            u'@blaugrana_apple そっか、まあ、会えたら会いましょう',
            u'きたく',
            u'まじでか。T.Tとか呼んだら来るんじゃね',
            u'ふらふらしてたら飲みのお誘いが来たので一旦帰る',
            u'おきた',
        ]

        end_tweets = [
            u'ウィッシュリストが増えていくが減る見込みがない',
            u'旅立つのは明日にしようかやっぱ',
            u'ちょっと旅立ってくる',
            u'休み長いから使わずに置いといてどっかで使いたい',
            u'スパ4買おうかなぁ',
            u'彼女がどうとか結婚がどうとか話してて俺はにこにこと笑っているしかなかった',
            u'金曜の反省を踏まえて水をがぶ飲みしている',
            u'飲みから帰宅中',
        ]

        tweets = self.log.get_tweets('yono', start)
        for i in xrange(len(tweets)):
            self.assert_(tweets[i], start_tweets[i])

        tweets = self.log.get_tweets('yono', start, end)
        all_tweets = start_tweets + end_tweets
        for i in xrange(len(tweets)):
            self.assert_(tweets[i], all_tweets[i])

    def test_download_tweets(self):
        aday = datetime.date(2010, 5, 3)
        start_tweets = [
            u'ついったーの話とか出たけどスルー',
            u'何もかも知らないふりしてる',
            u'@blaugrana_apple そっか、まあ、会えたら会いましょう',
            u'きたく',
            u'まじでか。T.Tとか呼んだら来るんじゃね',
            u'ふらふらしてたら飲みのお誘いが来たので一旦帰る',
            u'おきた',
        ]
        tweets = self.log._Twilog__download_tweets('yono', aday)
        for i in xrange(len(tweets)):
            self.assert_(tweets[i], start_tweets[i])

if __name__ == '__main__':
    unittest.main()
