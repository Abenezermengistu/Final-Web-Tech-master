import os
import psycopg2
import unittest as ut


POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

connection = psycopg2.connect(
                host=POSTGRES_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD)

create_table = """CREATE TABLE connections_db (
                    user_ip varchar(24) PRIMARY KEY,
                    num_conn int DEFAULT 1)"""
insert_row = "INSERT INTO connections_db (user_ip) VALUES (%s)"
select_all = "SELECT * FROM connections_db"

example_ip = '12.123.13.2'
cursor = connection.cursor()
cursor.execute(create_table)
cursor.execute(insert_row, (example_ip,))
cursor.execute(select_all)
row_count = cursor.rowcount
row = cursor.fetchone()

cursor.close()
connection.close()

class TestUnit(ut.TestCase):
    
    def test_number_of_rows(self):
        print('\nTesting number of rows')
        self.assertEqual(row_count, 1, 
                         msg=f"Wrong number of rows: {row_count}")
    
    def test_ip_stored(self):
        print('Testing ip stored')
        self.assertEqual(row[0], example_ip, 
                         msg=f"Wrong ip number stored: {row[0]}")

    def test_num_conn(self):
        print('Testing number of connections')
        self.assertEqual(row[1], 1, 
                         msg=f"Wrong number of connections: {row[1]}")


if __name__ == '__main__':
    ut.main()