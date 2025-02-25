import boto3
from config.config import DYNAMODB_TABLE_NAME

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def fetch_restaurants_by_ids(business_ids):
    try:
        keys = [{'business_id': id} for id in business_ids]
        response = dynamodb.batch_get_item(RequestItems={DYNAMODB_TABLE_NAME: {'Keys': keys}})
        return response['Responses'].get(DYNAMODB_TABLE_NAME, [])
    except Exception as e:
        print(f'Error fetching restaurants: {e}')
        return []

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
    business_ids = ['3D6UAhoKnF3A03rX_v5ngA', 'EM0JnhfXWwr_Nqw4_AjWAA', 'dEOv8_ivdHp85OK_TDQh_g']
    response = fetch_restaurants_by_ids(business_ids)
    print(response)