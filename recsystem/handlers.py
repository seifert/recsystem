
from shelter.core.web import BaseRequestHandler


class DummyHandler(BaseRequestHandler):

    def compute_etag(self):
        return None

    def get(self):
        self.write("recsystem - example handler")
