from duckdb import connect, DuckDBPyConnection
import streamlit as st
from exposition.tables import Table
from rich import print as rprint
from pandas import DataFrame


@st.cache_resource
def get_connection(database: str) -> DuckDBPyConnection:
    rprint(f"Connecting to DuckDB database: [bold magenta]{database}[/bold magenta]")
    return connect(database, read_only=True)


@st.cache_data
def fetch_data(tables: list[Table]) -> dict[str, DataFrame]:
    results = {}
    for table in tables:
        conn = get_connection(table.database)
        query = f"SELECT {', '.join(table.columns)} FROM {table.schema}.{table.name}"
        df = conn.execute(query).df()
        rprint(f"Fetched data from [bold yellow]{table.schema}.{table.name}[/bold yellow]")
        results[table.name] = df
    return results
