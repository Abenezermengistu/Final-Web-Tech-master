import requests
import json 
import unittest as ut
import os


class TestUnit(ut.TestCase):
    
    
    def test_geolocation(self):
        api_secret_key = os.getenv('API_SECRET_KEY')
        s = rf'http://api.ipstack.com/8.8.8.8?access_key={api_secret_key}'
        r = requests.get(s)
        geolocation_data = json.loads(r.content.decode('utf-8'))
        print(geolocation_data['ip'], geolocation_data['latitude'],
              geolocation_data['longitude'])
        self.assertIsNotNone(geolocation_data['latitude'], 
                             msg="Geolocation data retrieval FAILED!")


if __name__ == '__main__':
    ut.main()