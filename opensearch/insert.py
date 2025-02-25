import requests
from config.config import OPENSEARCH_URL, OPENSEARCH_HEADERS, OPENSEARCH_AUTH
from dynamodb.fetch import fetch_restaurants

def insert_restaurant(restaurant):
    url = f"{OPENSEARCH_URL}/restaurants/_doc/{restaurant['business_id']}"

    restaurant = {
        'business_id': restaurant.get('business_id', ''),
        'cuisine': restaurant.get('cuisine', ''),
        'location': restaurant.get('location', '')
    }

    response = requests.put(url, json=restaurant, headers=OPENSEARCH_HEADERS, auth=OPENSEARCH_AUTH)

    if response.status_code in [200, 201]:
        print(f"Indexed: {restaurant.get('business_id', '')} - {restaurant.get('cuisine', '')}")
    else:
        print(f"Error indexing {restaurant.get('business_id', '')}: {response.status_code} - {response.text}")

def insert_restaurants():
    restaurants = fetch_restaurants()

    if not restaurants:
        print('No restaurants found in DynamoDB')
        return

    for restaurant in restaurants:
        insert_restaurant(restaurant)
    
    print('Done!')

if __name__ == '__main__':
    # restaurant = {
    #     'business_id': 'uaFHoq-a5XqxF-bsOK9_Qg',
    #     'location': 'New York, NY',
    #     'cuisine': 'Chinese'
    # }
    # insert_restaurant(restaurant)
    insert_restaurants()