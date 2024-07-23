import os
import psycopg2
import unittest as ut
import requests
import json

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

#                google     facebook        youtube         wikipedia
ip_addr_list = ['8.8.8.8', '69.63.176.13', '74.125.65.91', '208.80.152.201']

cursor = connection.cursor()
cursor.execute(create_table)


api_secret_key = os.getenv('API_SECRET_KEY')

class IntegrationTest(ut.TestCase):
     
    def test_geolocation(self):
        for ip in ip_addr_list:
            s = rf'http://api.ipstack.com/{ip}?access_key={api_secret_key}'
            r = requests.get(s)
            d = json.loads(r.content.decode('utf-8'))
            self.assertIsNotNone(d['latitude'], 
                                 msg="Geolocation data retrieval FAILED!")
            cursor.execute(insert_row, (ip,))
        cursor.execute(select_all)
        
    def test_number_of_rows(self):
        row_count = cursor.rowcount
        self.assertEqual(row_count, len(ip_addr_list), 
                         msg=f"Wrong number of rows: {row_count}")    
    
    def test_ip_stored(self):
        print('Testing ip stored')
        for ip in ip_addr_list:
            row = cursor.fetchone()
            self.assertEqual(row[0], ip, 
                             msg=f"Wrong ip number stored: {row[0]} {ip}")
        cursor.close()
        connection.close()


if __name__ == '__main__':
    ut.main()
