from bigquery import BigQuery
import google.auth

def main():

    scopes = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]

    # get application default credentials
    credentials, project_id = google.auth.default(scopes=scopes)

    b = BigQuery(credentials)

    #query = 'select * from broad_bitstore_app.bits_billing_byfs_bitstore_historical where datetime = (select max(datetime) from broad_bitstore_app.bits_billing_byfs_bitstore_historical)'
    #query_results = b.query_job('broad-bitstore-app', query


    #for row in query_results:
        #print(row)


    dataset_ref = b.bigquery.Client().dataset('broad_bitstore_app', project='broad-bitstore-app')
    table_ref = dataset_ref.table('bits_billing_byfs_bitstore_historical')
    table = b.bigquery.Client().get_table(table_ref)
    # Load all rows from a table
    rows = b.bigquery.Client().list_rows(table)
    assert len(list(rows)) == table.num_rows

    # Load the first 10 rows
    #rows = b.bigquery.Client().list_rows(table, max_results=10)
    #assert len(list(rows)) == 10

    rows = b.bigquery.Client().list_rows(table)

   # field_names = [field.name for field in rows.schema]
   #format_string = '{!s:<16} ' * len(rows.schema)
    #print(format_string.format(*field_names))  # prints column headers
    #for row in rows:
        #print(format_string.format(*row))

    table_schema = b.get_table_schema('broad_bitstore_app', 'bits_billing_byfs_bitstore_historical', project_id='broad-bitstore-app')
    print(table_schema)






if __name__ == "__main__":
    main()
