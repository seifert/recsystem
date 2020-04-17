
from cached_property import cached_property
from shelter.core import context

from .rssfeeder import RssFeeder
from .storage import Storage


class Context(context.Context):

    def initialize(self):
        Storage.create_schema(**self.config.database)

        self.rss_feeder = RssFeeder(self.config.rss_feed)

    @cached_property
    def storage(self):
        return Storage(**self.config.database)
