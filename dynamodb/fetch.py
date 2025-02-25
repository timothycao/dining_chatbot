import boto3
from config.config import DYNAMODB_TABLE_NAME

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def fetch_restaurant(business_id):
    try:
        response = table.get_item(Key={'business_id': business_id})
        return response.get('Item', None)
    except Exception as e:
        print(f'Error fetching restaurant {business_id}: {e}')
        return None

def fetch_restaurants(limit=None):
    try:
        scan_kwargs = {}
        if limit:
            scan_kwargs['Limit'] = limit

        response = table.scan(**scan_kwargs)    # retrieves all by default if not given limit
        return response.get('Items', [])
    except Exception as e:
        print(f'Error fetching restaurants: {e}')
        return []

# Testing
if __name__ == '__main__':
    # response = fetch_restaurants(limit=5)
    response = fetch_restaurant('16ZnHpuaaBt92XWeJHCC5A')
    print(response)