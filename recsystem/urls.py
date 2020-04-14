
from tornado.web import URLSpec

from recsystem.handlers import DummyHandler


urls_default = (
    URLSpec(r'/', DummyHandler),
)
