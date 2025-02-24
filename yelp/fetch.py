import time
import requests
from config.config import YELP_API_URL, YELP_API_KEY

HEADERS = {'Authorization': f'Bearer {YELP_API_KEY}'}

def fetch_restaurants(cuisine, location, limit, offset):
    params = {
        'term': f'{cuisine} restaurants',
        'location': location,
        'limit': limit, # max 50
        'offset': offset
    }
    response = requests.get(YELP_API_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        # print(response.json())
        return response.json().get('businesses', [])
    else:
        print(f'Error: {response.status_code}, {response.text}')
        return []

def fetch_all_restaurants(cuisine, location, target_count):
    offset = 0
    all_restaurants = []
    while len(all_restaurants) < target_count:
        limit = min(50, target_count - len(all_restaurants))
        restaurants = fetch_restaurants(cuisine, location, limit, offset)
        
        if not restaurants: break   # stop if no more restaurants
        
        all_restaurants.extend(restaurants)
        offset += limit # move to next batch
        time.sleep(1)   # wait for 1 second to avoid rate limit
    
    return all_restaurants

# Testing
if __name__ == '__main__':
    cuisine = 'Italian'
    location = 'New York, NY'
    response = fetch_restaurants(cuisine, location, 1, 0)
    # response = fetch_all_restaurants(cuisine, location, 5)
    print(response)