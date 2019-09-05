"""BITStore App Main module."""

import jinja2
import json
import os
import webapp2
from datetime import datetime

import google.auth
from google.appengine.api import users

from bitstoreapiclient import BITStore
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
        request=request
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


class Usage(webapp2.RequestHandler):
    """Class for Usage page."""

    def get(self):
        """Return the usage page."""
        b = BITStore(**PARAMS)
        filesystems = b.get_filesystems()
        storageclasses = b.get_storageclasses()

        # Get the latest usage data from BQ
        latest_usages = b.get_latest_fs_usages()

        latest_usage_date = latest_usages[1]['datetime'].split("+")[0]

        # Make the list of dicts into a dict of dicts with fs value as key
        by_fs = {}
        for bq_row in latest_usages:
            if not bq_row['active']:
                continue
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
            'quotes_dict': quotes,
            'latest_usage_date': latest_usage_date,
            'storage_classes': storageclasses
            }

        template = jinja.get_template('usage.html')
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
        #quotes = {}
        for f in filesystems:
            server = f.get('server', None)
            quote = f.get('quote', None)
            # Assemble server dictionary
            if server in servers:
                servers[server].append(f)
            else:
                servers[server] = [f]
            # Assemble quote dictionary
            #if quote in quotes:
            #    quotes[quote].append(f)
            #else:
            #    quotes[quote] = [f]

        template_values = {
            'filesystems': filesystems,
            'servers': servers,
            #'quotes': quotes
        }
        template = jinja.get_template('filesystems.html')
        body = template.render(template_values)
        output = render_theme(body, self.request)
        self.response.write(output)


app = webapp2.WSGIApplication([
    ('/', Usage),
    #('/admin', AdminPage),
    ('/admin/filesystems', Filesystems),
    (r'/admin/filesystems/(\d+)', FilesystemPage),
    (r'/admin/filesystems/(\d+)/edit', FilesystemEditPage),
], debug=True)
