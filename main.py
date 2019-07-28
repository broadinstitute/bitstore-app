"""BITStore App Main module."""

import jinja2
import json
import os
import webapp2

from google.appengine.api import users

from bitstoreapiclient import BITStore

#from bits.google.services.bigquery import BigQuery

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

PARAMS = {
    'api_key': 'AIzaSyDzRhwd2xw77iyyp0acSEB3yNgNhdntAV0',
    # 'base_url': 'http://karlsson.c.broad-karlsson.internal:8081/_ah/api',
    # 'debug': True,
}


def is_dev():
    """Return true if this is the development environment."""
    dev = False
    if os.environ['SERVER_SOFTWARE'].startswith('Development'):
        dev = True
    return dev


def render_theme(body, request):
    """Render the main template header and footer."""
    template = jinja.get_template('theme.html')
    return template.render(
        body=body,
        is_admin=users.is_current_user_admin(),
        is_dev=is_dev(),
        request=request,
    )


class AdminPage(webapp2.RequestHandler):
    """Class for AdminPage."""

    def get(self):
        """Return the admin page."""
        template_values = {

        }
        template = jinja.get_template('admin.html')
        body = template.render(template_values)
        output = render_theme(body, self.request)
        self.response.write(output)


class FilesystemEditPage(webapp2.RequestHandler):
    """Class for FilesystemEditPage."""

    def get(self, filesystem_id):
        """Return the filesystem edit page."""
        b = BITStore(**PARAMS)
        filesystem = b.get_filesystem(filesystem_id)
        storageclasses = b.get_storageclasses()
        template = jinja.get_template('filesystem.html')
        body = template.render(
            edit=True,
            filesystem=filesystem,
            fs=filesystem['fs'],
            json=json.dumps(filesystem, indent=2, sort_keys=True),
            storageclasses=sorted(storageclasses, key=lambda x: x['name']),
        )
        output = render_theme(body, self.request)
        self.response.write(output)

    def post(self, filesystem_id):
        """Update a filesystem."""
        b = BITStore(**PARAMS)
        filesystem = b.get_filesystem(filesystem_id)
        post_data = dict(self.request.POST)

        print('Initial Post Data: %s' % (post_data))

        # check active
        if 'active' in post_data:
            post_data['active'] = True
        else:
            post_data['active'] = False

        print('Active Post Data: %s' % (post_data))

        # fields to potentially update
        fields = [
            'active',
            'primary_contact',
            'quote',
            'secondary_contact',
            'notes',
            'storage_class_id'
        ]

        # check post data for fields to update
        update = False
        for field in fields:
            if field in post_data:
                old = filesystem.get(field)
                new = post_data.get(field)
                if old != new:
                    if field == 'active':
                        if new == 'on':
                            new = True
                        if new == 'off':
                            new = False
                    filesystem[field] = new
                    update = True

        if update:
            # print(filesystem)
            response = b.bitstore.filesystems().insert(body=filesystem).execute()
            # print(response)

        self.redirect('/filesystems/%s' % (filesystem_id))


class FilesystemPage(webapp2.RequestHandler):
    """Class for FilesystemPage."""

    def get(self, filesystem_id):
        """Return the filesystem page."""
        b = BITStore(**PARAMS)
        filesystem = b.get_filesystem(filesystem_id)
        storageclasses = b.get_storageclasses()
        template = jinja.get_template('filesystem.html')
        body = template.render(
            edit=False,
            filesystem=filesystem,
            fs=filesystem['fs'],
            json=json.dumps(filesystem, indent=2, sort_keys=True),
            storageclasses=sorted(storageclasses, key=lambda x: x['name']),
        )
        output = render_theme(body, self.request)
        self.response.write(output)

class QuoteIndex(webapp2.RequestHandler):
    """Class for QuoteIndex page."""

    def get(self):
        """Return the quote page."""
        template_values = {'test': 'test'}

        template = jinja.get_template('quoteindex.html')
        body = template.render(template_values)

        output = render_theme(body, self.request)
        self.response.write(output)

class MainPage(webapp2.RequestHandler):
    """Class for MainPage."""

    def get(self):
        """Return the main page."""
        b = BITStore(**PARAMS)
        filesystems = b.get_filesystems()

        servers = {}
        for f in filesystems:
            server = f['server']
            if server in servers:
                servers[server].append(f)
            else:
                servers[server] = [f]

        template_values = {
            'filesystems': filesystems,
            'count': len(filesystems),
            'servers': servers,
        }
        template = jinja.get_template('index.html')
        body = template.render(template_values)
        output = render_theme(body, self.request)
        self.response.write(output)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage),
    ('/quote', QuoteIndex),
    (r'/filesystems/(\d+)', FilesystemPage),
    (r'/filesystems/(\d+)/edit', FilesystemEditPage),
], debug=True)
