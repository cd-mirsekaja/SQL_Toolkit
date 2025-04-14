#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SQL_Toolkit/src/SQL_Toolkit/sql_utils.py
import pandas as pd
import os

def remove_database(db_file: str):
	"""
	Removes a database file if it exists.

	Args:
		db_file (str): Path to the SQLite database file.
	"""
	if os.path.isfile(db_file):
		os.remove(db_file)
		print(f"Existing database file '{db_file}' removed.")
	else:
		print(f"Database file '{db_file}' does not exist.")

def infer_sqlite_type(dtype):
	"""
	Infers the SQLite column type from a pandas dtype.

	Args:
		dtype (pandas dtype): The pandas dtype to infer from.

	Returns:
		str: The corresponding SQLite column type.
	"""
	if pd.api.types.is_integer_dtype(dtype):
		return "INTEGER"
	elif pd.api.types.is_numeric_dtype(dtype):
		return "NUMERIC"
	elif pd.api.types.is_float_dtype(dtype):
		return "REAL"
	elif pd.api.types.is_bool_dtype(dtype):
		return "BOOLEAN"
	elif pd.api.types.is_datetime64_any_dtype(dtype):
		return "DATETIME"
	elif pd.api.types.is_object_dtype(dtype):
		return "BLOB"
	else:
		return "TEXT"