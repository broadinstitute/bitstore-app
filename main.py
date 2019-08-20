"""BITStore App Main module."""

import jinja2
import json
import os
import webapp2

#import requests
#import requests_toolbelt.adapters.appengine
#requests_toolbelt.adapters.appengine.monkeypatch(validate_certificate=True)

import google.auth
from google.appengine.api import users

from bitstoreapiclient import BITStore
#from bigquery import BigQuery
from config import api, api_key, base_url, debug

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

PARAMS = {
    'api': api,
    'api_key': api_key,
    'base_url': base_url,
    'debug': debug,
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


#def post_request(url, headers=None, data=None):
#    """Make a post using requests"""
#    r = requests.post(url=url, headers=headers, data=data)
#
#    return r.text

def assemble_query_result_list(query_result):
    """
    Creates a list of dicts with the keys being the schema field,
    and the value being the value of that field
    """
    schema = query_result.schema
    list_of_rows = []
    for row in query_result:
        i = 0
        row_dict = {}
        for attr in row:
            row_dict[schema[i].name] = attr
            i += 1

        list_of_rows.append(row_dict)

    return list_of_rows


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

        self.redirect('/admin/filesystems/%s' % (filesystem_id))


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
        b = BITStore(**PARAMS)
        filesystems = b.get_filesystems()

        # Get the latest usage data from BQ
        latest_usages = b.get_latest_fs_usages()

        # Make the list of dicts into a dict of dicts with fs value as key
        by_fs = {}
        for bq_row in latest_usages:
            by_fs[bq_row['fs']] = bq_row

        # assemble a dictionary using each quote as a key
        # WHY ARE THERE 2 OF THESE?!?!?
        #quotes = {}
        #for fs, fs_value in by_fs.items():
        #    if fs_value['quote'] in quotes:
        #        quotes[fs_value['quote']][fs] = fs_value
        #    else:
        #        quotes[fs_value['quote']] = {fs: fs_value}

        # assemble a dictionary using each quote as a key
        quotes = {}
        for f in by_fs:
            fs_row = by_fs[f]
            quote = fs_row['quote']
            if quote in quotes:
                quotes[quote].append(fs_row)
            else:
                quotes[quote] = [fs_row]

        template_values = {
            'filesystems': filesystems,
            'by_fs': by_fs,
            'quotes_dict': quotes
            }

        template = jinja.get_template('quoteindex.html')
        body = template.render(template_values)

        output = render_theme(body, self.request)
        self.response.write(output)


class Filesystems(webapp2.RequestHandler):
    """Class for Filesystems page."""

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
        template = jinja.get_template('filesystems.html')
        body = template.render(template_values)
        output = render_theme(body, self.request)
        self.response.write(output)

app = webapp2.WSGIApplication([
    ('/', QuoteIndex),
    #('/', Filesystems),
    #('/admin', AdminPage),
    ('/admin/filesystems', Filesystems),
    (r'/admin/filesystems/(\d+)', FilesystemPage),
    (r'/admin/filesystems/(\d+)/edit', FilesystemEditPage),
], debug=True)
