#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SQL_Toolkit/src/SQL_Toolkit/make_sql.py

import pandas as pd
import sqlite3, csv, os
from .sql_utils import remove_database, infer_sqlite_type

def excel_to_sqlite(input_file: str, db_file: str, remove_existing: bool=False):
	"""
	Converts an Excel file with any number of sheets to an SQLite database.
	Each sheet is converted to a separate table in the database.
	Each column in the sheet is converted to a column in the table.

	Args:
		input_file (str): Path to the Excel file.
		db_file (str): Path to the SQLite database file.
		remove_existing (bool): Whether to remove the database file if it already exists.
	"""

	try:
		# load all sheets into a dictionary of dataframes
		excel_data = pd.read_excel(input_file, sheet_name=None)

		# raise an error it the file is empty
		if not excel_data:
			raise ValueError("Excel file contains no sheets.")

		# remove existing database file if requested
		if remove_existing and os.path.exists(db_file):
			print(f"Removing existing database file: {db_file}")
			remove_database(db_file)

		# establish connection to the database
		db_conn = sqlite3.connect(db_file)
		cursor = db_conn.cursor()

		# iterate through sheets and create tables
		for sheet_name, df in excel_data.items():
			# sanitize sheet name for use as table name (replace spaces, special chars)
			table_name = ''.join(e for e in sheet_name if e.isalnum() or e == '_')

			# create table statement (inferring data types)
			columns = ', '.join(f'"{col}" {infer_sqlite_type(dtype)}' for col, dtype in df.dtypes.items())
			create_table_sql = f"CREATE TABLE IF NOT EXISTS \"{table_name}\" ({columns})"

			# execute query to create table
			cursor.execute(create_table_sql)

			# insert data
			df.to_sql(table_name, db_conn, if_exists='append', index=False)

		# commit changes and close connection
		db_conn.commit()
		db_conn.close()
		print(f"Excel data from '{input_file}' successfully loaded into \n'{db_file}'.")

	# handle exceptions
	except FileNotFoundError:
		print(f"Error: Input file '{input_file}' not found.")
	except ValueError as e:
		print(f"Error: {e}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")


def csv_to_sqlite(input_file: str, db_file: str, remove_existing: bool=False):
	"""
	Converts a CSV file to an SQLite database.

	Args:
		input_file (str): Path to the CSV file.
		db_file (str): Path to the SQLite database file.
		remove_existing (bool): Whether to remove the database file if it already exists.
	"""

	try:
		# automatically detect the delimiter
		with open(input_file, 'r') as f:
			sample = f.read(1024)
			print(sample)
			sniffer = csv.Sniffer()
			print(sniffer)
			dialect = sniffer.sniff(sample=sample)
			delimiter=dialect.delimiter
			print(delimiter)

		# load CSV into a DataFrame
		csv_data = pd.read_csv(input_file, delimiter=delimiter)

		# raise an error if the file is empty
		if csv_data.empty:
			raise ValueError("CSV file is empty.")

		# remove database file if requested
		if remove_existing and os.path.exists(db_file):
			print(f"Removing existing database file: {db_file}")
			print(remove_database)
			remove_database(db_file)

		# establish connection to the database
		db_conn = sqlite3.connect(db_file)
		cursor = db_conn.cursor()

		# sanitize file name for use as table name (replace spaces, special chars)
		table_name = os.path.splitext(os.path.basename(input_file))[0]
		table_name = ''.join(e for e in table_name if e.isalnum() or e == '_')

		# create table statement (inferring data types)
		columns = ', '.join(f'"{col}" {infer_sqlite_type(dtype)}' for col, dtype in csv_data.dtypes.items())
		create_table_sql = f"CREATE TABLE IF NOT EXISTS \"{table_name}\" ({columns})"

		# execute query to create table
		cursor.execute(create_table_sql)

		# insert data
		csv_data.to_sql(table_name, db_conn, if_exists='append', index=False)

		# commit changes and close connection
		db_conn.commit()
		db_conn.close()
		print(f"CSV data from '{input_file}' successfully loaded into \n'{db_file}'.")

	# handle exceptions
	except FileNotFoundError:
		print(f"Error: Input file '{input_file}' not found.")
	except ValueError as e:
		print(f"Error: {e}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")