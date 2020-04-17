
import collections
import socket
import time

import feedparser

Entry = collections.namedtuple('Entry', ['published', 'guid', 'url', 'title'])


class RssFeeder(object):

    def __init__(self, rss_feed_config):
        self.rss_feed_config = rss_feed_config

    def iter_entries(self):
        socket.setdefaulttimeout(self.rss_feed_config.timeout)
        try:
            rss = feedparser.parse(self.rss_feed_config.url)

            if 'bozo' in rss and rss.bozo:
                reason = str(rss.bozo_exception)
                raise Exception('Fetch RSS failed: {}'.format(reason))
            elif not rss.entries:
                raise Exception('Fetch RSS failed: no entries')

            for entry in rss.entries:
                yield Entry(
                    published=int(time.mktime(entry.published_parsed)),
                    guid=entry.id, url=entry.link, title=entry.title)
        finally:
            socket.setdefaulttimeout(None)
