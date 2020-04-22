
from tornado.web import URLSpec

from recsystem.handlers import EntitiesList, Event


urls_default = (
    URLSpec(r'/', EntitiesList),
    URLSpec(r'/event', Event),
)
