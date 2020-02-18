"""BITStore API Client class file."""

from bits.appengine.endpoints import Endpoints
from bigquery import BigQuery

class BITStore(Endpoints.Client):
    """BITStore class."""

    def __init__(
        self,
        api_key=None,
        base_url='http://localhost:8080',
        # base_url='https://broad-bitstore-api-dev.appspot.com',
        api='bitstore',
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

    # # get a group of items from memcache
    # def get_memcache_group(self, group):
    #     """Return a list of a group of memcache items."""
    #     group_list = memcache.get(group)
    #     if group_list is None:
    #         return None

    #     # create a list of buckets of items
    #     buckets = []
    #     for item in group_list:
    #         bucket = item[0]
    #         if bucket not in buckets:
    #             buckets.append(bucket)

    #     # for each bucket, retrieve items
    #     items = []
    #     for b in buckets:
    #         bkey = '%s:%s' % (group, b)
    #         bitems = memcache.get(bkey)
    #         if bitems:
    #             items += bitems

    #     return items

    # # save a large group of items in memcache
    # def save_memcache_group(self, group, items, key):
    #     """Save a list of memcache items too large for one key."""
    #     buckets = {}
    #     items_list = []

    #     # create a dict of buckets of items and a list of item names
    #     for item in items:
    #         name = item[key]

    #         # put item into the appropriate bucket
    #         bucket = name[0]
    #         if bucket not in buckets:
    #             buckets[bucket] = [item]
    #         else:
    #             buckets[bucket].append(item)

    #         # add name to items_list
    #         items_list.append(name)

    #     # save each of the buckets to memcache
    #     for b in buckets:
    #         key = '%s:%s' % (group, b)
    #         memcache.add(key, buckets[b], self.memcache_time)

    #     # save the list of items to memcache
    #     memcache.add(group, items_list, self.memcache_time)

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
        # filesystems = self.get_memcache_group('filesystems')
        # if filesystems is not None:
        #     return filesystems
        params = {'limit': 1000}
        filesystems = self.get_paged_list(self.bitstore.filesystems(), params)
        # self.save_memcache_group('filesystems', filesystems, 'server')
        return filesystems

    def get_filesystem(self, filesystem_id):
        """Return a single filesystem."""
        return self.bitstore.filesystems().get(id=filesystem_id).execute()

    def get_storageclasses(self):
        """Return a list of StorageClases from BITSdb."""
        # storageclasses = memcache.get('storageclasses')
        # if storageclasses is not None:
        #     return storageclasses
        params = {'limit': 1000}
        storageclasses = self.get_paged_list(self.bitstore.storageclasses(), params)
        # memcache.add('storageclasses', storageclasses, self.memcache_time)
        return storageclasses

    # # BQ queries
    # def query_historical_usage_bq(self, json_data, function):
    #     """Query BQ table for the chosen dates set of filesystem data."""
    #     # print(inspect(self.bitstore))
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': 'bearer {}'.format(self.generate_id_token())
    #     }

    #     # Assemble the headers and data into a HTTP request and run fetch
    #     table_list = requests.post(
    #         url=function,
    #         headers=headers,
    #         data=json.dumps(json_data),
    #     ).content

    #     return table_list

    def get_fs_usages(self, datetime=None, select='*'):
        """Query BQ table for the chosen dates set of filesystem data."""
        if not datetime:
            datetime = '(select max(datetime) from broad_bitstore_app.bits_billing_byfs_bitstore_historical)'
        dataset = 'broad_bitstore_app'
        table_name = 'bits_billing_byfs_bitstore_historical'
        query_string = ' '.join([
            'select {SELECT}'.format(SELECT=select),
            'from {DATASET}.{TABLE_NAME}'.format(DATASET=dataset, TABLE_NAME=table_name),
            'where datetime = {DATE_TIME}'.format(DATE_TIME=datetime)
        ])

        # fs_usage = json.loads(self.query_historical_usage_bq(data, 'https://us-central1-broad-bitstore-app.cloudfunctions.net/QueryBQTableBitstore'))
        # if not datetime:
        #     self.save_memcache_group('fs_usage_latest', fs_usage, 'server')
        # else:
        #     self.save_memcache_group(datetime, fs_usage, 'server')

        bq = BigQuery(project='broad-bitstore-app')
        fs_usage = bq.get_query_results(query_string)

        return fs_usage


    def get_fs_usage_all_time(self, fs, select='*'):
        """Query BQ table for all historical usage of defined filesystem."""
        dataset = 'broad_bitstore_app'
        table_name = 'bits_billing_byfs_bitstore_historical'
        query_string = ' '.join([
            'select {SELECT}'.format(SELECT=select),
            'from {DATASET}.{TABLE_NAME}'.format(DATASET=dataset, TABLE_NAME=table_name),
            'where fs = "{fs}"'.format(fs=fs)
        ])
        bq = BigQuery(project='broad-bitstore-app')
        fs_usage = bq.get_query_results(query_string)

        return fs_usage