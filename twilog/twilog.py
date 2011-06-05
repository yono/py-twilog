#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from HTMLParser import HTMLParser
import time
import urllib2
import urlparse
import re

class Tweet(object):
    """
    つぶやき（post）を扱うクラス
    """
    text = None
    date = None

    def __init__(self, text, date):
        self.text = text
        self.date = date

class Twilog(object):
    """
    Twilog を扱うクラス
    """

    BASEURL = "http://twilog.org/"

    def __init__(self):
        self.parser = TwilogParser()

    def get_html(self, url):
        time.sleep(5)
        fp = urllib2.urlopen(url)
        html = unicode(fp.read(), 'utf-8', 'ignore')
        return html

    def get_url(self, user, aday=''):
        url = self.BASEURL + user
        target_date = aday if aday else datetime.datetime.today()
        return url + '/date-' + self.get_url_date(target_date)

    def _get_tweets(self, user, start='', end=''):
        results = []
        time_results = []
        if start == end == '':
            results, time_results = self.get_tweets_from_web(user)
        elif start == '' and end:
            results, time_results = self.get_tweets_from_web(user, end)
        elif start and end == '':
            results, time_results = self.get_tweets_from_web(user, start)
        else:
            from_date, to_date = start, end
            if from_date > to_date:
                from_date, to_date = to_date, from_date
            current_date = from_date
            while current_date <= to_date:
                tweets, times = self.get_tweets_from_web(user, current_date)
                results.extend(tweets)
                time_results.extend(times)
                current_date += datetime.timedelta(days=1)
        return (results, time_results)

    def get_tweets(self, user, start='', end=''):
        tweets, time_results = self._get_tweets(user, start=start, end=end)
        return tweets

    def get_tweets_verbose(self, user, start='', end=''):
        tweets, time_results = self._get_tweets(user, start=start, end=end)
        i = 0
        result = []
        for i in xrange(len(tweets)):
            result.append(Tweet(tweets[i], time_results[i]))
        return result

    def get_tweets_from_web(self, user, aday=''):
        url = self.get_url(user, aday)
        html = self.get_html(url)
        self.parser.sentences = []
        self.parser.times = []
        self.parser.feed(html)
        tweets = self.parser.sentences
        _times = self.parser.times
        times = []
        for _time in _times:
            aday_obj = aday
            if aday == '':
                aday_obj = datetime.datetime.today()
            times.append(datetime.datetime(aday_obj.year, aday_obj.month, 
                aday_obj.day, _time.hour, _time.minute, _time.second))
        return (tweets, times)

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
        self.time_flag = False
        self.words = []
        self.sentences = []
        self.times = []
        self.is_times = re.compile(r"\d{2}:\d{2}:\d{2}")

    def handle_starttag(self, tag, attrs):
        attrs_dic = dict(attrs)

        if tag == 'p' and 'class' in attrs_dic:
            if attrs_dic['class'] == 'tl-text':
                self.flag = True
        if tag == 'a':
            self.time_flag = True

    def handle_data(self, data):
        if self.flag:
            self.words.append(data)
        if self.time_flag and self.is_times.match(data):
            self.times.append(datetime.datetime.strptime(data, '%H:%M:%S'))

    def handle_endtag(self, tag):
        if tag == 'p':
            sentence = ''.join(self.words)
            if sentence != '':
                self.sentences.append(sentence)
            self.words = []
            self.flag = False
        if tag == 'a':
            self.time_flag = False

if __name__ == '__main__':
    log = Twilog()
    tweets = log.get_tweets('yono')
    for tweet in tweets:
        print tweet

    print '------ Today\'s Tweets ------'

    tweets = log.get_tweets('yono', datetime.date.today(),
                            datetime.date.today())
    for tweet in tweets:
        print tweet
