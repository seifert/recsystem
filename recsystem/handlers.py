
import json

import mako.template

from shelter.core.web import BaseRequestHandler


class EntitiesList(BaseRequestHandler):

    template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>${rss | h}</title>
            <style type="text/css">
                ul {list-style: none outside none; padding-left: 0px}
                li {padding-top: 0.25em}
            </style>
        </head>
        <%!
            import json
        %>
        <body>
            <h1>${rss | h}</h1>
            % if entities:
            <ul>
            % for ent in entities:
                <%
                    event = json.dumps({
                        'alpha': ent.id,
                        'betas': [e.id for e in entities if e.id != ent.id],
                    })
                %>
                <li>
                    ${ent.published | h}
                    <button data-event="${event | h}" onclick="vote(this)">
                        +1
                    </button>
                    ${ent.title | h}
                </li>
            % endfor
            </ul>
            % endif
            <script>
                function vote(element) {
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("POST", "/event", true);
                    xhttp.send(element.dataset.event);
                }
            </script>
        </body>
        </html>
    '''

    def get(self):
        self.write(
            mako.template.Template(self.template).render(
                rss=self.context.config.rss_feed.url,
                entities=self.context.storage.entities_list(limit=25),
            )
        )


class Event(BaseRequestHandler):

    def post(self):
        event = json.loads(self.request.body)
        self.context.alpha_beta_counter.inc_alpha(event['alpha'])
        for entity_id in event['betas']:
            self.context.alpha_beta_counter.inc_beta(entity_id)
