
from cached_property import cached_property
from shelter.core import config


class Config(config.Config):

    @cached_property
    def database(self):
        return self._settings.DATABASE
