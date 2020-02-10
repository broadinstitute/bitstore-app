"""Google BigQuery API."""

# import os
# import datetime
# import json
from google.cloud import bigquery


class BigQuery():
    """BigQuery class."""

    def __init__(self, project):
        """Initialize a class instance."""
        self.bq = bigquery.Client(project=project)


    def submit_query(self, query_string):
        """Query a table with a query argument."""
        query_job = self.bq.query(query_string)

        return query_job.result()


    def assemble_query_result_list(self, query_result):
        """
        Creates a list of dicts with the keys being the schema field,
        and the value being the value of that field.
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


    def get_query_results(self, query_string):
        """Main function, returns query results in list form."""
        query_result = self.submit_query(query_string)
        assembled_results = self.assemble_query_result_list(query_result)

        # return json.dumps(assembled_results, indent=2, default=str)
        return assembled_results
