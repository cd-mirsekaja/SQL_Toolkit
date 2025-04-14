#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SQL_Toolkit/src/SQL_Toolkit/read_sql.py

import sqlite3, os

def query_database(db_file: str, query: str, params: tuple=()):
    """
    Executes a query against an SQLite database and returns the results.

    Args:
        db_file (str): Path to the SQLite database file.
        query (str): SQL query to execute.
        params (tuple): Parameters to pass to the query (optional).

    Returns:
        list: A list of tuples representing the query results, or None if an error occurs.
    """
    try:
        if not os.path.isfile(db_file):
            raise FileNotFoundError(f"Database file '{db_file}' not found.")

        db_conn = sqlite3.connect(db_file)
        cursor = db_conn.cursor()

        cursor.execute(query, params)
        results = cursor.fetchall()

        db_conn.close()
        return results

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_rows_by_param(db_file: str, table: str, column: str, param: str=""):
    """
    Retrieves IDs from the taxonomy table for a given scientific name.

    Args:
        db_file (str): Path to the SQLite database file.
        table (str): The table to search.
        param (str): The scientific name to search for.

    Returns:
        list: A list of IDs (integers) matching the scientific name, or None if not found or an error occurs.
    """
    query = f"SELECT * FROM {table} WHERE {column} = ?"
    results = query_database(db_file, query, (param,))
    if results:
        return [row for row in results]  # Extract IDs from tuples
    else:
        return None