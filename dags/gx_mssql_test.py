from pendulum import datetime
from airflow.decorators import dag
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from include.gx_custom import GreatExpectationsOperator
from include.great_expectations.checkpoints.strawberry_checkpoint_config import (
    strawberry_checkpoint,
)

MSSQL_CONN_ID = "mssql_default"
POSTGRES_CONN_ID = "postgres_default"


@dag(
    start_date=datetime(2023, 7, 1),
    schedule=None,
    catchup=False,
)
def gx_mssql_test():
    create_table_ms = MsSqlOperator(
        task_id="create_table_ms",
        mssql_conn_id=MSSQL_CONN_ID,
        sql="""
            CREATE TABLE strawberries (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100),
                amount INT
            );

            INSERT INTO strawberries (id, name, amount)
            VALUES ('001', 'Strawberry Order 1', 10),
                ('002', 'Strawberry Order 2', 5),
                ('003', 'Strawberry Order 3', 8),
                ('004', 'Strawberry Order 4', 3),
                ('005', 'Strawberry Order 5', 12);
            """,
    )

    gx_validate_ms = GreatExpectationsOperator(
        task_id="gx_validate_ms",
        data_context_root_dir="include/great_expectations",
        checkpoint_config=strawberry_checkpoint,
        expectation_suite_name="dbo.strawberry_suite",
        return_json_dict=True,
        execution_engine="SqlAlchemyExecutionEngine",
    )

    gx_validate_ms_use_conn_id = GreatExpectationsOperator(
        task_id="gx_validate_ms_use_conn_id",
        data_context_root_dir="include/great_expectations",
        conn_id=MSSQL_CONN_ID,
        data_asset_name="dbo.strawberries",
        expectation_suite_name="strawberry_suite",
        return_json_dict=True,
    )

    drop_table_ms = MsSqlOperator(
        task_id="drop_table_ms",
        mssql_conn_id=MSSQL_CONN_ID,
        sql="""
            DROP TABLE strawberries;
            """,
    )

    create_table_pg = PostgresOperator(
        task_id="create_table_pg",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
            CREATE TABLE strawberries (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100),
                amount INT
            );

            INSERT INTO strawberries (id, name, amount)
            VALUES ('001', 'Strawberry Order 1', 10),
                ('002', 'Strawberry Order 2', 5),
                ('003', 'Strawberry Order 3', 8),
                ('004', 'Strawberry Order 4', 3),
                ('005', 'Strawberry Order 5', 12);
            """,
    )

    gx_validate_pg = GreatExpectationsOperator(
        task_id="gx_validate_pg",
        conn_id=POSTGRES_CONN_ID,
        data_context_root_dir="include/great_expectations",
        data_asset_name="strawberries",
        expectation_suite_name="strawberry_suite",
        return_json_dict=True,
    )

    drop_table_pg = PostgresOperator(
        task_id="drop_table_pg",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
            DROP TABLE strawberries;
            """,
    )

    create_table_ms >> [gx_validate_ms, gx_validate_ms_use_conn_id] >> drop_table_ms
    create_table_pg >> gx_validate_pg >> drop_table_pg


gx_mssql_test()
