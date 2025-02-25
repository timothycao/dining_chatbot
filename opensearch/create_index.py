import requests
from config.config import OPENSEARCH_URL, OPENSEARCH_HEADERS, OPENSEARCH_AUTH

def create_index():
    url = f'{OPENSEARCH_URL}/restaurants'

    index_config = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 1
        },
        'mappings': {
            'properties': {
                'business_id': { 'type': 'keyword' },
                'cuisine': { 'type': 'keyword' },
                'location': { 'type': 'text' }  # allows flexible location search
            }
        }
    }

    response = requests.put(url, json=index_config, headers=OPENSEARCH_HEADERS, auth=OPENSEARCH_AUTH)

    if response.status_code in [200, 201]:
        print(f'Index "restaurants" created successfully')
    else:
        print(f'Error creating index: {response.status_code} - {response.text}')

if __name__ == '__main__':
    create_index()