"""Google BigQuery API."""

from google.cloud import bigquery


class BigQuery():
    """BigQuery class."""

    def __init__(self, project, credentials):
        """Initialize a class instance."""
        self.bq = bigquery.Client(project=project, credentials=credentials)

    def bq_query(self, query):
        """Query a table with a query argument"""
        query_job = self.bq.query(query)

        return query_job.result()

    def assemble_query_result_list(self, query_result):
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
