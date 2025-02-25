import json
import random
from config.config import SES_RECEIVER_EMAIL
from sqs.manage import send_message, receive_message, delete_message
from opensearch.search import search_restaurants
from dynamodb.fetch import fetch_restaurants_by_ids
from ses.send import send_email

def fetch_random_restaurants(cuisine, location, count):
    # Query OpenSearch with given cuisine
    restaurants = search_restaurants(cuisine, location, size=100)

    if not restaurants:
        return None
    
    # Get random restaurants from results
    random_restaurants = random.sample(restaurants, count)
    # print('RANDOM RESTAURANTS:', random_restaurants)

    # Fetch and return full data from DynamoDB
    business_ids = [restaurant['_source']['business_id'] for restaurant in random_restaurants]
    return fetch_restaurants_by_ids(business_ids)

def lambda_handler(event, context):
    message = receive_message()

    if not message:
        print('There are no messages in the queue.')
        return
    
    # Extract message data
    body = json.loads(message.get('Body', '{}'))
    cuisine = body.get('Cuisine')
    location = body.get('Location')
    email = body.get('Email')

    if not cuisine or not location or not email:
        print('Invalid request: missing cuisine, location, or email')
        delete_message(message['ReceiptHandle'])
        return

    # Fetch restaurant recommendations
    restaurants = fetch_random_restaurants(cuisine, location, 3)

    if not restaurants:
        print(f'No {cuisine} restaurants found.')
        delete_message(message['ReceiptHandle'])
        return
    
    # Send email with restaurant recommendation
    send_email(email, restaurants, cuisine, location)

    # Delete processed SQS message
    delete_message(message['ReceiptHandle'])

# Testing
if __name__ == '__main__':
    data = {
        'Location': 'Brooklyn',
        'Cuisine': 'Italian',
        'PartySize': '2',
        'DiningTime': '7:00 PM',
        'Email': SES_RECEIVER_EMAIL
    }

    send_message(data)
    lambda_handler(None, None)