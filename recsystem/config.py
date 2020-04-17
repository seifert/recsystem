
import collections

from cached_property import cached_property
from shelter.core import config

RSSFeedConfig = collections.namedtuple('RSSFeedConfig', ['url', 'timeout'])


class Config(config.Config):

    @cached_property
    def database(self):
        return self._settings.DATABASE

    @cached_property
    def rss_feed(self):
        return RSSFeedConfig(
            self._settings.RSS_FEED['url'],
            self._settings.RSS_FEED.get('timeout'),
        )
