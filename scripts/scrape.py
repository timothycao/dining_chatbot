from yelp.fetch import fetch_all_restaurants
from dynamodb.store import store_restaurants

def scrape_restaurants(cuisines, locations, target_count):
    for location in locations:
        for cuisine in cuisines:
            print(f'Fetching {target_count} {cuisine} restaurants in {location}...')
            restaurants = fetch_all_restaurants(cuisine, location, target_count)

            print(f'Storing {len(restaurants)} results in DynamoDB...')
            store_restaurants(restaurants, cuisine)

            print('Done!')

if __name__ == '__main__':
    cuisines = ['Italian', 'Mexican', 'Chinese']
    locations = ['New York, NY']
    target_count = 5
    # target_count = 100
    scrape_restaurants(cuisines, locations, target_count)