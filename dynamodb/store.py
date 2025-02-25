import decimal
from datetime import datetime, timezone
import boto3
from config.config import DYNAMODB_TABLE_NAME

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def store_restaurants(restaurants, cuisine):
    # with table.batch_writer() as batch: # batch does not support conditional expressions
        for restaurant in restaurants:
            try:
                # batch.put_item(
                table.put_item(
                    Item={
                        # Required Fields
                        'business_id': restaurant.get('id', ''),
                        'name': restaurant.get('name', ''),
                        'address': ', '.join(restaurant.get('location', {}).get('display_address', [])),
                        # 'coordinates': restaurant.get('coordinates', {'latitude': 0.0, 'longitude': 0.0}),  # DynamoDB does not support float
                        'coordinates': {
                            'latitude': decimal.Decimal(str(restaurant.get('coordinates', {}).get('latitude', 0.0))),
                            'longitude': decimal.Decimal(str(restaurant.get('coordinates', {}).get('longitude', 0.0)))
                        },
                        'review_count': restaurant.get('review_count', 0),
                        # 'rating': restaurant.get('rating', 0.0),    # DynamoDB does not support float
                        'rating': decimal.Decimal(str(restaurant.get('rating', 0.0))),
                        'zip_code': restaurant.get('location', {}).get('zip_code', ''),
                        'inserted_at_timestamp': str(datetime.now(timezone.utc)),

                        # Additional Fields (for ElasticSearch and Filtering)
                        'location': f"{restaurant.get('location', {}).get('city', '')}, {restaurant.get('location', {}).get('state', '')}",
                        'cuisine': cuisine
                        # 'categories': [category.get('alias', '') for category in restaurant.get('categories', [])],
                        # 'business_hours': restaurant.get('business_hours', [])
                    },
                    ConditionExpression='attribute_not_exists(business_id)' # avoid duplicate insertions
                )
            except Exception as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    print(f"Skipping duplicate: {restaurant.get('name', '')}")
                else:
                    print(f"Error inserting {restaurant.get('name', '')}: {e}")

# Testing
if __name__ == '__main__':
    restaurants = [
        {
            'id': '16ZnHpuaaBt92XWeJHCC5A',
            'name': 'Olio e Più',
            'review_count': 6367,
            'categories': [
                {'alias': 'pizza', 'title': 'Pizza'},
                {'alias': 'italian', 'title': 'Italian'},
                {'alias': 'cocktailbars', 'title': 'Cocktail Bars'}
            ],
            'rating': 4.5,
            'coordinates': {'latitude': 40.73406231935954, 'longitude': -73.99999980859876},
            'location': {
                'address1': '3 Greenwich Ave',
                'address2': None,
                'address3': '',
                'city': 'New York',
                'zip_code': '10014',
                'country': 'US',
                'state': 'NY',
                'display_address': ['3 Greenwich Ave', 'New York, NY 10014']
            }
        }
    ]
    cuisine = 'Italian'
    response = store_restaurants(restaurants, cuisine)
    print(response)