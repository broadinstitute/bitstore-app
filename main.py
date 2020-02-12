"""BITStore App Main module."""

import json
import datetime
import time

import google.auth

from bits.appengine import AppEngine
from bits.appengine.theme import Theme
from bitstoreapiclient import BITStore
# from google.cloud import firestore

from flask import Flask, render_template, redirect, request, abort


todays_date = datetime.datetime.today()

_, project = google.auth.default()

DEBUG = True

debug_user = {
    'email': 'daltschu@broadinstitue.org',
    'id': '117063677019555687611',
    'admin': True
}

# Initialize the flask app
app = Flask(__name__)

# Create an object called appengine from the bits-appengine module
appengine = AppEngine(
    config_project=project,
    debug_user=debug_user,
    user_project=project,
)

PARAMS = appengine.config().get_config('bitstore')

def extended_footer():
    """Render the extended footer for the main template."""
    with app.app_context():
        body = render_template('extended-footer.html')
        return body

theme = Theme(
    appengine=appengine,
    app_name='Bitstore App',
    links=[

        {'name': 'Usage', 'url': '/'},
        {'name': 'Admin Filesystems', 'url': '/admin/filesystems', 'admin': True},
        {'name': 'Users', 'url': '/admin/users', 'admin': True},
    ],
    repo='bitstore-app',
    body_class="container-fluid",
    extended_footer=extended_footer(),
    topnav_padding=True
)


# Shared functions
def fs_list_to_dict(filesystems):
    """
    Convert a list of filesystem objects to a dict
    with each key being the FS and the object being the object
    """
    fs_dict = {}
    for fs in filesystems:
        fs_dict[fs['fs']] = fs

    return fs_dict


def storage_class_list_to_dict(storage_classes):
    """
    Convert a list of storage class objects to a dict
    with each key being the id and the object being the object
    """
    sc_dict = {}
    for sc in storage_classes:
        sc_dict[sc['id']] = sc

    return sc_dict


def convert_to_tebi(bytes):
    """Convert from bytes to tebibytes (Meaning 1024^4)."""
    tebibytes_converted = round(((((float(bytes) / 1024) / 1024) / 1024) / 1024), 4)
    return tebibytes_converted


# Jinja Custom Templates
@app.template_filter('strptime')
def strptime_filter(s):
    """Jinja filter for strptime."""
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


@app.template_filter('strftime')
def strftime_filter(s):
    """Jinja filter for strftime."""
    return datetime.datetime.strftime(s, "%Y-%m-%d")

# @app.errorhandler(403)
# def unauthorized_boot():
#     return 'Unauthorized!', 403

# Flask Page Routes
@app.route('/admin/filesystems/<int:filesystem_id>/edit', methods=['GET', 'POST'])
def filesystem_edit_page(filesystem_id):
    """Flask parser for FilesystemEditPage."""
    b = BITStore(**PARAMS)
    filesystem = b.get_filesystem(filesystem_id)
    storageclasses = b.get_storageclasses()
    user = appengine.user()

    # Check if user is admin, if not 403
    if not user.admin:
        # redirect(boot_if_not_admin())
        abort(403)

    # Handle a GET
    if request.method == 'GET':
        """Return the filesystem edit page."""

        body = render_template(
            'admin-filesystem.html',
            edit=True,
            filesystem=filesystem,
            fs=filesystem['fs'],
            json=json.dumps(filesystem, indent=2, sort_keys=True),
            storageclasses=sorted(storageclasses, key=lambda x: x['name']),
        )
        output = theme.render_theme(body)
        return output

    # Handle a POST
    if request.method == 'POST':
        # This handles updating a filesystem
        post_data = dict(request.form)
        print('Initial Post Data: {}'.format(post_data))

        # check active
        if 'active' in post_data:
            post_data['active'] = True
        else:
            post_data['active'] = False

        print('Active Post Data: {}'.format(post_data))

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
            response = b.bitstore.filesystems().insert(body=filesystem).execute()
            # print(response)

        return redirect('/admin/filesystems/{}'.format(filesystem_id))


@app.route('/admin/filesystems/<int:filesystem_id>')
def filesystem_page(filesystem_id):
    """Return the filesystem page."""
    b = BITStore(**PARAMS)
    filesystem = b.get_filesystem(filesystem_id)
    storageclasses = b.get_storageclasses()

    user = appengine.user()

    # Check if user is admin, if not 403
    if not user.admin:
        # redirect(boot_if_not_admin())
        abort(403)

    body = render_template(
        'admin-filesystem.html',
        edit=False,
        filesystem=filesystem,
        fs=filesystem['fs'],
        json=json.dumps(filesystem, indent=2, sort_keys=True),
        storageclasses=sorted(storageclasses, key=lambda x: x['name']),
    )

    output = theme.render_theme(body)
    return output


@app.route('/')
def usage_page():
    """Return the usage page."""
    # Get passed in args
    date_time = request.args.get('date_time')
    tic1 = time.perf_counter()
    b = BITStore(**PARAMS)
    toc1 = time.perf_counter()
    tic2 = time.perf_counter()
    filesystems = b.get_filesystems()
    toc2 = time.perf_counter()
    tic3 = time.perf_counter()
    storageclasses = b.get_storageclasses()
    toc3 = time.perf_counter()
    
    print(f"Time to get connection to firestore {toc1 - tic1:0.4f} seconds")
    print(f"Time to query db for filesystems {toc2 - tic2:0.4f} seconds")
    print(f"Time to query database for storage classes {toc3 - tic3:0.4f} seconds")

    # Assemble the filesystem and storage class lists into dicts
    filesys_dict = fs_list_to_dict(filesystems)
    sc_dict = storage_class_list_to_dict(storageclasses)

    
    if date_time:
        # Get the data from the supplied date string like 'yy-mm-dd'
        sql_datetime = '(select max(datetime) from broad_bitstore_app.bits_billing_byfs_bitstore_historical where DATE(datetime) = "{}" )'.format(date_time)
        latest_usages = b.get_fs_usages(datetime=sql_datetime)
    else:
        # Or else just get the latest usage data from BQ
        latest_usages = b.get_fs_usages()

    # # If date doesnt exist, kick person back up to latest date
    # if not latest_usages:
    #     latest_usages = b.get_fs_usages()

    # latest_usage_date = latest_usages[1]['datetime'].split("+")[0]
    latest_usage_date = latest_usages[1]['datetime'].strftime('%Y-%m-%d %H:%M:%S')

    # Make the list of dicts into a dict of dicts with fs value as key
    by_fs = {}
    for bq_row in latest_usages:
        # Skip over inactive filesystems for this table
        if not bq_row['active']:
            continue

        # Assign the dictionary fs key to the bq sql result row values
        by_fs[bq_row['fs']] = bq_row

        # Calculate overhead usages as a separate value
        byte_usage_overhead = bq_row.get('byte_usage', 0)
        if not byte_usage_overhead:
            byte_usage_overhead = 0
        byte_usage_without_overhead = bq_row.get('byte_usage_no_overhead', 0)
        # If overhead DOESNT exist, set the overhead usage to 0 and set the share usage to the byte_usage value
        if not byte_usage_without_overhead:
            byte_usage_without_overhead = 0
            by_fs[bq_row['fs']]['share_usage'] = byte_usage_overhead
            overhead_usage = 0
        # If overhead DOES exist, set the overhead usage to usage - overhead and share usage to usage_without_overhead
        else:
            by_fs[bq_row['fs']]['share_usage'] = byte_usage_without_overhead
            overhead_usage = byte_usage_overhead - byte_usage_without_overhead

        by_fs[bq_row['fs']]['overhead_usage'] = overhead_usage

        # Calculate out the total usage value
        dr_byte_usage = by_fs[bq_row['fs']].get('dr_byte_usage', 0)
        if not dr_byte_usage:
            dr_byte_usage = 0
        snapshot_byte_usage = by_fs[bq_row['fs']].get('snapshot_byte_usage', 0)
        if not snapshot_byte_usage:
            snapshot_byte_usage = 0

        total_usage = byte_usage_overhead + snapshot_byte_usage
        by_fs[bq_row['fs']]['total_usage'] = total_usage

        if bq_row['fs'] in filesys_dict:
            if filesys_dict[bq_row['fs']].get('mountpoints'):
                # This uuuuugly
                by_fs[bq_row['fs']]['mountpoint'] = filesys_dict[bq_row['fs']]['mountpoints'][0].get('mountpoint')
            if filesys_dict[bq_row['fs']].get('storage_class_id'):
                fs_sc_id = filesys_dict[bq_row['fs']].get('storage_class_id')
                if fs_sc_id in sc_dict:
                    by_fs[bq_row['fs']]['storage_class'] = sc_dict[fs_sc_id].get('name')

    available_dates = [todays_date - datetime.timedelta(days=x) for x in range(40)]

    body = render_template(
        'usage.html',
        filesystems=filesys_dict,
        by_fs=by_fs,
        latest_usage_date=latest_usage_date,
        available_dates=available_dates
    )

    output = theme.render_theme(body)
    return output


@app.route('/usage-graphs')
def usage_graph_page():
    """Return the graph page."""
    b = BITStore(**PARAMS)

    passed_fs = request.args.get('fs')

    print(passed_fs)

    all_time_usage = b.get_fs_usage_all_time(fs=passed_fs)

    fs_usage_list = []
    for usage in all_time_usage:
        new_usage = {}
        # Calculate overhead usages as a separate value
        byte_usage_overhead = usage.get('byte_usage', 0)
        if not byte_usage_overhead:
            byte_usage_overhead = 0
        byte_usage_without_overhead = usage.get('byte_usage_no_overhead', 0)
        # If overhead DOESNT exist, set the overhead usage to 0 and set the share usage to the byte_usage value
        if not byte_usage_without_overhead:
            byte_usage_without_overhead = 0
            new_usage['share_usage'] = convert_to_tebi(byte_usage_overhead)
            overhead_usage = 0
        # If overhead DOES exist, set the overhead usage to usage - overhead and share usage to usage_without_overhead
        else:
            new_usage['share_usage'] = convert_to_tebi(byte_usage_without_overhead)
            overhead_usage = byte_usage_overhead - byte_usage_without_overhead

        new_usage['overhead_usage'] = convert_to_tebi(overhead_usage)

        # Calculate out the total usage value
        dr_byte_usage = usage.get('dr_byte_usage', 0)
        if not dr_byte_usage:
            dr_byte_usage = 0
            
        snapshot_byte_usage = usage.get('snapshot_byte_usage', 0)
        if not snapshot_byte_usage:
            snapshot_byte_usage = 0
            
        quota_allocation = usage.get('quota_allocation', 0)
        if not quota_allocation:
            quota_allocation = 0

        total_usage = byte_usage_overhead + snapshot_byte_usage
        new_usage['total_usage'] = convert_to_tebi(total_usage)
        new_usage['datetime'] = usage.get('datetime')
        new_usage['quota_allocation'] = convert_to_tebi(quota_allocation)
        new_usage['snapshot_byte_usage'] = convert_to_tebi(snapshot_byte_usage)
        new_usage['dr_usage'] = convert_to_tebi(dr_byte_usage)

        fs_usage_list.append(new_usage)

    all_time_usage_sorted_by_date = sorted(fs_usage_list, key=lambda x: x['datetime'])

    body = render_template(
        'usage-graphs.html',
        fs_name=passed_fs,
        fs_usage_sorted=all_time_usage_sorted_by_date
    )

    output = theme.render_theme(body)
    return output


@app.route('/admin/filesystems')
def admin_filesystems_page():
    """Return the main page."""
    b = BITStore(**PARAMS)
    filesystems = b.get_filesystems()
    user = appengine.user()

    # Check if user is admin, if not 403
    if not user.admin:
        # redirect(boot_if_not_admin())
        abort(403)

    servers = {}
    for f in filesystems:
        server = f.get('server', None)
        # Assemble server dictionary
        if server in servers:
            servers[server].append(f)
        else:
            servers[server] = [f]

    body = render_template(
        'admin-filesystems.html',
        filesystems=filesystems,
        servers=servers,
    )
        
    output = theme.render_theme(body)
    return output

@app.route('/admin/users')
def admin_users():
    """Return the admin users page."""
    # view the users list
    return theme.admin_users_page(page_name='Users')


@app.route('/admin/users/add', methods=['GET', 'POST'])
def admin_users_add():
    """Return the admin users add page."""
    # view the add user page
    if request.method == 'GET':
        return theme.admin_users_add_page(page_name='Add User')
    # add a new user
    elif request.method == 'POST':
        return theme.admin_users_add_user()


@app.route('/admin/users/<uid>', methods=['GET', 'POST'])
def admin_users_edit(uid):
    """Return the admin users edit page."""
    # delete a user
    if request.method == 'GET':
        return theme.admin_users_edit_page(uid, page_name='Edit User {}'.format(uid))
    elif request.method == 'POST':
        return theme.admin_users_edit_user(uid)


@app.route('/admin/users/<uid>/delete')
def admin_users_delete(uid):
    """Return the admin users delete page."""
    return theme.admin_users_delete(uid)


if __name__ == '__main__':
    from flask import send_file  # noqa

    @app.route('/favicon.ico')
    def favicon():
        """Return the favicon."""
        return send_file('favicon.ico', mimetype='image/x-icon')

    @app.route('/styles.css')
    def styles():
        """Return styles.css."""
        return send_file('styles.css', mimetype='text/css')

    app.run(host='0.0.0.0', port=8085, debug=DEBUG)