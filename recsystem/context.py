
import collections
import weakref

from cached_property import cached_property, cached_property_with_ttl
from shelter.core import context

from .rssfeeder import RssFeeder
from .storage import Storage


class AlphaBetaCounter(object):

    def __init__(self):
        self.alpha = collections.defaultdict(float)
        self.beta = collections.defaultdict(float)

    def inc_alpha(self, entity_id):
        self.alpha[entity_id] += 1

    def inc_beta(self, entity_id):
        self.beta[entity_id] += 1


class Context(context.Context):

    def initialize(self):
        Storage.create_schema(**self.config.database)

        self.rss_feeder = RssFeeder(self.config.rss_feed)

    @cached_property
    def storage(self):
        return Storage(**self.config.database)

    @cached_property_with_ttl(ttl=5)
    def alpha_beta_counter(self):
        c = AlphaBetaCounter()
        weakref.finalize(c, self.storage.save_alphas_betas, c.alpha, c.beta)
        return c
