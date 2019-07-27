"""Google BigQuery API."""

from google.cloud import bigquery
from googleapiclient.discovery import build


class BigQuery():
    """Directory class."""

    def __init__(self, credentials):
        """Initialize a class instance."""
        self.bigquery = bigquery
        self.bq = build('bigquery', 'v2', credentials=credentials)

    def create_table(self, project, dataset, body):
        """Create a BigQuery table."""
        params = {
            'projectId': project,
            'datasetId': dataset,
            'body': body,
        }
        return self.bq.tables().insert(**params).execute()

    def delete_table(self, project, dataset, table):
        """Create a BigQuery table."""
        params = {
            'projectId': project,
            'datasetId': dataset,
            'tableid': table,
        }
        return self.bq.tables().delete(**params).execute()

    def get_dataset(self, project, dataset):
        """Return a BigQuery dataset."""
        params = {
            'projectId': project,
            'datasetId': dataset,
        }
        return self.bq.datasets().get(**params).execute()

    def get_datasets(self, project):
        """Return list of BigQuery datasets."""
        datasets = self.bq.datasets()
        request = datasets.list(projectId=project)
        return self.get_list_items(datasets, request, 'datasets')

    def get_projects(self):
        """Return list of BigQuery projects."""
        projects = self.bq.projects()
        request = projects.list(maxResults=10)
        return self.get_list_items(projects, request, 'projects')

    def get_tabledata(
            self,
            project,
            dataset,
            table,
            maxResults=None,
            startIndex=None
    ):
        """Return list of BigQuery tabledata."""
        params = {
            'projectId': project,
            'datasetId': dataset,
            'tableId': table,
            'maxresults': maxResults,
            'startIndex': startIndex,
        }
        return self.bq.tabledata().list(**params).execute().get('rows', [])

    def get_table(self, project, dataset, table):
        """Return a BigQuery table."""
        params = {
            'projectId': project,
            'datasetId': dataset,
            'tableId': table,
        }
        return self.bq.tables().get(**params).execute()

    def get_tables(self, project, dataset):
        """Return list of BigQuery tables."""
        params = {
            'projectId': project,
            'datasetId': dataset,
        }
        tables = self.bq.tables()
        request = tables.list(**params)
        return self.get_list_items(tables, request, 'tables')

    def query_job(self, project, query):
        """Return results of a BigQuery query job."""
        params = {
            'projectId': project,
            'body': {
                'query': query,
                'useLegacySql': False,
            },

        }
        return self.bq.jobs().query(**params).execute().get('rows', [])

    def insert_job(self, project, body, media_body, media_mime_type):
        """Insert BigQuery job."""
        params = {
            'projectId': project,
            'body': body,
            'media_body': media_body,
            'media_mime_type': media_mime_type,
        }
        return self.bq.jobs().insert(**params).execute()

    def insert_tabledata(self, project, dataset, table, data):
        """Insert BigQuery tabledata."""
        params = {
            'projectId': project,
            'datasetId': dataset,
            'tableId': table,
            'body': data,
        }
        return self.bq.tabledata().insertAll(**params).execute()


    def _get_project_id(self, project_id=None):
        """ Get new project_id
            Default is self.project_id, which is the project client authenticate to.
            A new project_id is specified when client wants to authenticate to 1 project,
            but run jobs in a different project.
            Parameters
            ----------
            project_id : str
                BigQuery project_id
            Returns
            -------
            project_id: BigQuery project_id
        """
        if project_id is None:
            project_id = self.project_id
        return project_id



    def _transform_row(self, row, schema):
        """Apply the given schema to the given BigQuery data row.
        Parameters
        ----------
        row
            A single BigQuery row to transform
        schema : list
            The BigQuery table schema to apply to the row, specifically
            the list of field dicts.
        Returns
        -------
        dict
            Mapping schema to row
        """

        log = {}

        # Match each schema column with its associated row value
        for index, col_dict in enumerate(schema):
            col_name = col_dict['name']
            row_value = row['f'][index]['v']

            if row_value is None:
                log[col_name] = None
                continue

            # Recurse on nested records
            if col_dict['type'] == 'RECORD':
                row_value = self._recurse_on_row(col_dict, row_value)

            # Otherwise just cast the value
            elif col_dict['type'] == 'INTEGER':
                row_value = int(row_value)

            elif col_dict['type'] == 'FLOAT':
                row_value = float(row_value)

            elif col_dict['type'] == 'BOOLEAN':
                row_value = row_value in ('True', 'true', 'TRUE')

            elif col_dict['type'] == 'TIMESTAMP':
                row_value = float(row_value)

            log[col_name] = row_value

        return log

    def get_table_schema(self, dataset, table, project_id=None):
        """Return the table schema.
        Parameters
        ----------
        dataset : str
            The dataset containing the `table`.
        table : str
            The table to get the schema for
        project_id: str, optional
            The project of the dataset.
        Returns
        -------
        list
            A ``list`` of ``dict`` objects that represent the table schema. If
            the table doesn't exist, None is returned.
        """
        project_id = self._get_project_id(project_id)

        try:    
            result = self.bigquery.tables().get(
                projectId=project_id,
                tableId=table,
                datasetId=dataset).execute(num_retries=self.num_retries)
        except Exception:
             pass

        return result['schema']['fields']
