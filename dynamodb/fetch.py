import boto3
from config.config import DYNAMODB_TABLE_NAME

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def fetch_restaurants(limit=None):
    scan_kwargs = {}
    if limit:
        scan_kwargs['Limit'] = limit

    response = table.scan(**scan_kwargs)    # retrieves all by default if not given limit
    return response.get('Items', [])

# Testing
if __name__ == '__main__':
    response = fetch_restaurants(limit=5)
    print(response)