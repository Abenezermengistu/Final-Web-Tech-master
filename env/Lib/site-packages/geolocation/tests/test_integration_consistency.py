import os
import unittest as ut
import requests
import json


class IntegrationTestConsistency(ut.TestCase):
    
    def test_geolocation_consistency(self):
        api_secret_key = os.getenv('API_SECRET_KEY')
        google_latitude = '37.38801956176758'
        s = rf'http://api.ipstack.com/8.8.8.8?access_key={api_secret_key}'
        r = requests.get(s)
        d = json.loads(r.content.decode('utf-8'))
        self.assertEqual(d['latitude'], float(google_latitude), msg="Latitude not consistant")


if __name__ == '__main__':
    ut.main()
