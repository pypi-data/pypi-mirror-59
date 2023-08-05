import psycopg2
from mobilitydb.psycopg import register
from mobilitydb.examples.db_connect import psycopg_connect

connection = None

try:
	# Set the connection parameters to PostgreSQL
	connection = psycopg_connect()
	connection.autocommit = True

	# Register MobilityDB data types
	register(connection)

	cursor = connection.cursor()

	######################
	# TBOX
	######################

	select_query = "select * from tbl_tbox order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tbox table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tbox =", row[1])
		if not row[1]:
			print("")
		else:
			print("tmin =", row[1].tmin, "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tbox_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tbox_temp
		(
		  k integer PRIMARY KEY,
		  box tbox
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tbox_temp (k, box) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tbox_temp table")

	######################
	# STBOX
	######################

	select_query = "select * from tbl_stbox order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_stbox table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("stbox =", row[1])
		if not row[1]:
			print("")
		else:
			print("tmin =", row[1].tmin, "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_stbox_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_stbox_temp
		(
		  k integer PRIMARY KEY,
		  box stbox
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_stbox_temp (k, box) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_stbox_temp table")

	print("\n****************************************************************")

except (Exception, psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL", error)

finally:

	if connection:
		connection.close()
