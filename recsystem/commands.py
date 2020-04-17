
from shelter.core.commands import BaseCommand


class FetchRss(BaseCommand):

    name = "fetch_rss"
    help = "fetch new entries from rss feed"

    def command(self):
        self.logger.info('Fetch RSS')
        counter = 0
        for entry in self.context.rss_feeder.iter_entries():
            try:
                self.context.storage.insert_entity(
                    entry.published, entry.guid, entry.url, entry.title)
            except self.context.storage.DuplicateEntry:
                pass
            else:
                counter += 1
        self.logger.info('Fetched %d entities', counter)
