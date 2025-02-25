import requests
from config.config import OPENSEARCH_URL, OPENSEARCH_HEADERS, OPENSEARCH_AUTH

def search_restaurants(cuisine=None, location=None, size=10):
    """
    Searches OpenSearch for restaurants by cuisine, location, or both.
    
    :param cuisine: (str) Cuisine type (e.g., 'Italian')
    :param location: (str) City or state (e.g., 'New York', 'NY')
    :param size: (int) Number of results to return (default: 10)
    """
    
    url = f'{OPENSEARCH_URL}/restaurants/_search'

    # Build query conditions
    conditions = []
    
    if cuisine:
        conditions.append({'match': {'cuisine': cuisine}})
    
    if location:
        conditions.append({'match': {'location': location}})
    
    query = {
        'size': size,  
        'query': {
            'bool': {
                # Return all restaurants if no conditions provided
                'must': conditions if conditions else [{'match_all': {}}]
            }
        }
    }

    response = requests.get(url, json=query, headers=OPENSEARCH_HEADERS, auth=OPENSEARCH_AUTH)

    if response.status_code == 200:
        results = response.json().get('hits', {}).get('hits', [])
        print(f'Found {len(results)} restaurants matching query:')
        for result in results:
            print(f"{result['_source']['business_id']} - {result['_source']['cuisine']} - {result['_source']['location']}")
    else:
        print(f'Error searching: {response.status_code} - {response.text}')

# Testing
if __name__ == '__main__':
    search_restaurants(cuisine='Italian', location='New York')
    search_restaurants(cuisine='Chinese', location='NY')