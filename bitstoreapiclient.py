"""BITStore API Client class file."""

# import base64
# import httplib
# import httplib2
import json
import sys
# import time

# if sys.version_info >= (3, 0):
#     from urllib.parse import urlencode
# else:
#     from urllib import urlencode

# support for requests
# import requests
# import requests_toolbelt.adapters.appengine
# requests_toolbelt.adapters.appengine.monkeypatch()

# import google.auth
# from bits.google import Google
from bits.appengine.endpoints import Endpoints


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class BITStore(Endpoints.Client):
    """BITStore class."""

    def __init__(
        self,
        api_key=None,
        base_url='http://localhost:8080',
        # base_url='https://broad-bitstore-api-dev.appspot.com/_ah/api',
        api='bitstore-dev',
        version='v1',
        verbose=False,
    ):
        """Initialize a BITSdb class instance."""
        Endpoints.Client.__init__(
            self,
            api_key=api_key,
            base_url=base_url,
            api=api,
            version=version,
            verbose=verbose,
        )
        self.bitstore = self.service
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #     """Initialize a class instance."""
    #     self.api_key = api_key
    #     self.debug = debug
    #     self.memcache_time = memcache_time

    #     # set scopes for the bitsdb service connection
    #     self.scopes = [
    #         'https://www.googleapis.com/auth/cloud-platform',
    #         'https://www.googleapis.com/auth/userinfo.email',
    #         'https://www.googleapis.com/auth/userinfo.profile',
    #     ]

    #     # get application default credentials
    #     self.credentials, self.project_id = google.auth.default(scopes=self.scopes)

    #     # get service account email
    #     self.service_account_email = self.credentials.service_account_email

    #     # request a Google ID token based on the service account email
    #     self.id_token = self.get_id_token(self.service_account_email)

    #     # create credentials from that id_token
    #     credentials = client.AccessTokenCredentials(
    #         self.id_token,
    #         'my-user-agent/1.0'
    #     )

    #     # create an httplib2 Http object
    #     # self.http = credentials.authorize(httplib2.Http(memcache, timeout=60))
    #     self.http = credentials.authorize(httplib2.Http(timeout=120))

    #     # print out the access token
    #     if self.debug:
    #         credentials = AppAssertionCredentials(self.scopes)
    #         access_token = credentials.get_access_token().access_token
    #         print('Access Token: %s' % (access_token))

    #     # build the discovery_url
    #     discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (
    #         base_url,
    #         api,
    #         api_version
    #     )

    #     # create the service connection to bitsdb
    #     self.bitstore = build(
    #         api,
    #         api_version,
    #         developerKey=api_key,
    #         discoveryServiceUrl=discovery_url,
    #         http=self.http,
    #         # credentials=self.credentials,
    #     )

    # def auth_service_account_json(self):
    #     """Authorize service account credentials stored in a bucket."""
    #     # get application identity
    #     app_id = app_identity.get_application_id()

    #     bucket = '%s.appspot.com' % (app_id)
    #     filename = 'service_account.json'

    #     # get app assertion credentials
    #     credentials = AppAssertionCredentials(self.scopes)

    #     # connect to storage api
    #     storage = build('storage', 'v1', credentials=credentials)
    #     objects = storage.objects()

    #     # get storage object data
    #     try:
    #         body = objects.get(bucket=bucket, object=filename).execute()
    #     except Exception as e:
    #         if e._get_reason() == 'Not Found':
    #             print('ERROR: service account key [gs://%s/%s] not found!' % (
    #                 bucket,
    #                 filename,
    #             ))
    #         else:
    #             print('ERROR: getting service account key [gs://%s/%s]!' % (
    #                 bucket,
    #                 filename,
    #             ))
    #         return

    #     if 'metadata' not in body:
    #         print('WARNING: "metadata" not found in gs://%s/%s' % (
    #             bucket,
    #             filename,
    #         ))
    #         body['metadata'] = {'encrypted': False}
    #         objects.update(bucket=bucket, object=filename, body=body).execute()

    #     print(json.dumps(body, indent=2, sort_keys=True))

    # def generate_jwt(self, service_account_email):
    #     """Generate a signed JSON Web Token using the Google App Engine default service account."""
    #     now = int(time.time())

    #     header_json = json.dumps({
    #         "typ": "JWT",
    #         "alg": "RS256"
    #     })

    #     payload_json = json.dumps({
    #         # issued at - time
    #         "iat": now,
    #         # expires after one hour.
    #         "exp": now + 3600,
    #         # iss is the service account email.
    #         "iss": service_account_email,
    #         # target_audience is the URL of the target service.
    #         "target_audience": "https://broad-bitstore-api.appspot.com/web-client-id",
    #         # aud must be Google token endpoints URL.
    #         "aud": "https://www.googleapis.com/oauth2/v4/token"
    #     })

    #     header_and_payload = '{}.{}'.format(
    #         base64.urlsafe_b64encode(header_json),
    #         base64.urlsafe_b64encode(payload_json))
    #     (_, signature) = app_identity.sign_blob(header_and_payload)
    #     signed_jwt = '{}.{}'.format(
    #         header_and_payload,
    #         base64.urlsafe_b64encode(signature))

    #     return signed_jwt

    # def get_id_token(self, service_account_email):
    #     """Request a Google ID token using a JWT."""
    #     params = urlencode({
    #         'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    #         'assertion': self.generate_jwt(service_account_email)
    #     })
    #     headers = {"Content-Type": "application/x-www-form-urlencoded"}
    #     conn = httplib.HTTPSConnection("www.googleapis.com")
    #     conn.request("POST", "/oauth2/v4/token", params, headers)
    #     res = json.loads(conn.getresponse().read())
    #     conn.close()
    #     return res['id_token']

    def get_paged_list(self, request, params={}):
        """Return a list of all items from a request."""
        response = request.list().execute()
        #print("response!!!", response)
        if not response:
            return []
        items = response.get('items', [])
        pageToken = response.get('nextPageToken')
        while pageToken:
            params['pageToken'] = pageToken
            response = request.list(**params).execute()
            items += response.get('items', [])
            pageToken = response.get('nextPageToken')
        return items

    # get a group of items from memcache
    def get_memcache_group(self, group):
        """Return a list of a group of memcache items."""
        group_list = memcache.get(group)
        if group_list is None:
            return None

        # create a list of buckets of items
        buckets = []
        for item in group_list:
            bucket = item[0]
            if bucket not in buckets:
                buckets.append(bucket)

        # for each bucket, retrieve items
        items = []
        for b in buckets:
            bkey = '%s:%s' % (group, b)
            bitems = memcache.get(bkey)
            if bitems:
                items += bitems

        return items

    # save a large group of items in memcache
    def save_memcache_group(self, group, items, key):
        """Save a list of memcache items too large for one key."""
        buckets = {}
        items_list = []

        # create a dict of buckets of items and a list of item names
        for item in items:
            name = item[key]

            # put item into the appropriate bucket
            bucket = name[0]
            if bucket not in buckets:
                buckets[bucket] = [item]
            else:
                buckets[bucket].append(item)

            # add name to items_list
            items_list.append(name)

        # save each of the buckets to memcache
        for b in buckets:
            key = '%s:%s' % (group, b)
            memcache.add(key, buckets[b], self.memcache_time)

        # save the list of items to memcache
        memcache.add(group, items_list, self.memcache_time)

    # convert a list to a dict
    def to_json(self, items, key='id'):
        """Return a dict of items."""
        data = {}
        for i in items:
            k = i.get(key)
            data[k] = i
        return data

    # filesystems
    def get_filesystems(self):
        """Return a list of Filesystems from BITSdb."""
        filesystems = self.get_memcache_group('filesystems')
        if filesystems is not None:
            return filesystems
        params = {'limit': 1000}
        filesystems = self.get_paged_list(self.bitstore.filesystems(), params)
        self.save_memcache_group('filesystems', filesystems, 'server')
        return filesystems

    def get_filesystem(self, filesystem_id):
        """Return a single filesystem."""
        return self.bitstore.filesystems().get(id=filesystem_id).execute()

    def get_storageclasses(self):
        """Return a list of StorageClases from BITSdb."""
        storageclasses = memcache.get('storageclasses')
        if storageclasses is not None:
            return storageclasses
        params = {'limit': 1000}
        storageclasses = self.get_paged_list(self.bitstore.storageclasses(), params)
        memcache.add('storageclasses', storageclasses, self.memcache_time)
        return storageclasses

    # BQ queries
    def query_historical_usage_bq(self, json_data, function):
        """Query BQ table for the chosen dates set of filesystem data."""

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'bearer {}'.format(self.id_token)
        }

        # Assemble the headers and data into a HTTP request and run fetch
        table_list = urlfetch.fetch(
            method=urlfetch.POST,
            url=function,
            headers=headers,
            payload=json.dumps(json_data),
            deadline=15
        ).content

        return table_list

    def get_fs_usages(self, datetime=None, select='*'):
        if datetime:
            fs_usage = self.get_memcache_group('datetime')
        else:
            fs_usage = self.get_memcache_group('fs_usage_latest')
        if fs_usage is not None:
            return fs_usage
        if not datetime:
            datetime = '(select max(datetime) from broad_bitstore_app.bits_billing_byfs_bitstore_historical)'
        data = {
            'select': select,
            'dataset': 'broad_bitstore_app',
            'table_name': 'bits_billing_byfs_bitstore_historical',
            'date_time': datetime
        }
        fs_usage = json.loads(self.query_historical_usage_bq(data, 'https://us-central1-broad-bitstore-app.cloudfunctions.net/QueryBQTableBitstore'))
        if not datetime:
            self.save_memcache_group('fs_usage_latest', fs_usage, 'server')
        else:
            self.save_memcache_group(datetime, fs_usage, 'server')
        return fs_usage

    def get_fs_usage_all_time(self, fs, select='*'):
        data = {
            'select': select,
            'dataset': 'broad_bitstore_app',
            'table_name': 'bits_billing_byfs_bitstore_historical',
            'fs': fs
        }
        fs_usage = json.loads(self.query_historical_usage_bq(data, 'https://us-central1-broad-bitstore-app.cloudfunctions.net/QueryBQTableBitstoreHistorical'))

        return fs_usage