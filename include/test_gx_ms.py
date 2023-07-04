import os

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/mssql_yaml_example.py imports">
import great_expectations as gx
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.core.yaml_handler import YAMLHandler

yaml = YAMLHandler()
# </snippet>

CONNECTION_STRING = f"mssql+pyodbc://sa:AdminMicrosoft123@host.docker.internal:1433/master?driver=ODBC Driver 17 for SQL Server&charset=utf8&autocommit=true"

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/mssql_yaml_example.py get_context">
context = gx.get_context()
# </snippet>

datasource_yaml = r"""
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/mssql_yaml_example.py datasource config">
name: my_mssql_datasource
class_name: Datasource
execution_engine:
  class_name: SqlAlchemyExecutionEngine
  connection_string: mssql+pyodbc://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>?driver=<DRIVER>&charset=utf&autocommit=true
data_connectors:
   default_runtime_data_connector_name:
       class_name: RuntimeDataConnector
       batch_identifiers:
           - default_identifier_name
   default_inferred_data_connector_name:
       class_name: InferredAssetSqlDataConnector
       include_schema_name: true
# </snippet>
"""

# Please note this override is only to provide good UX for docs and tests.
# In normal usage you'd set your path directly in the yaml above.
datasource_yaml = datasource_yaml.replace(
    "mssql+pyodbc://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>?driver=<DRIVER>&charset=utf&autocommit=true",
    CONNECTION_STRING,
)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/mssql_yaml_example.py test datasource config">
context.test_yaml_config(datasource_yaml)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/mssql_yaml_example.py add datasource config">
context.add_datasource(**yaml.load(datasource_yaml))
# </snippet>

# Here is a RuntimeBatchRequest using a query
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/mssql_yaml_example.py load data with query">
batch_request = RuntimeBatchRequest(
    datasource_name="my_mssql_datasource",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="strawberries",  # this can be anything that identifies this data
    runtime_parameters={"query": "SELECT * FROM strawberries"},
    batch_identifiers={"default_identifier_name": "default_identifier"},
)
context.add_or_update_expectation_suite(expectation_suite_name="strawberry_suite")
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name="strawberry_suite"
)
print(validator.head())

