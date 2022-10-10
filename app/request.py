import requests
import random
BASE_URL = 'http://127.0.0.1:5000'

def make_request(url):
    response = requests.post(f"{BASE_URL}{url}")
    return response.json()


city = make_request('/api/cities')
print(city)
print(make_request(f'/api/10most-expensive-flats/{random.choice(city)}'))

