import json
import random
from config.config import SES_RECEIVER_EMAIL
from sqs.manage import send_message, receive_message, delete_message
from opensearch.search import search_restaurants
from dynamodb.fetch import fetch_restaurant
from ses.send import send_email

def fetch_random_restaurant(cuisine):
    # Query OpenSearch with given cuisine
    restaurants = search_restaurants(cuisine, location=None, size=100)

    if not restaurants:
        return None
    
    # Get random restaurant from results
    random_restaurant = random.choice(restaurants)
    print('RANDOM RESTAURANT:', random_restaurant)

    # Fetch and return full data from DynamoDB
    business_id = random_restaurant['_source']['business_id']
    return fetch_restaurant(business_id)

def lambda_handler(event, context):
    message = receive_message()

    if not message:
        print('There are no messages in the queue.')
        return
    
    # Extract message data
    body = json.loads(message.get('Body', '{}'))
    cuisine = body.get('Cuisine')
    email = body.get('Email')

    if not cuisine or not email:
        print('Invalid request: missing cuisine or email')
        delete_message(message['ReceiptHandle'])
        return

    # Fetch restaurant recommendation
    restaurant = fetch_random_restaurant(cuisine)

    if not restaurant:
        print(f'No {cuisine} restaurants found.')
        delete_message(message['ReceiptHandle'])
        return
    
    # Send email with restaurant recommendation
    send_email(email, restaurant)

    # Delete processed SQS message
    delete_message(message['ReceiptHandle'])

# Testing
if __name__ == '__main__':
    data = {
        'Location': 'New York',
        'Cuisine': 'Italian',
        'PartySize': '2',
        'DiningTime': '7:00 PM',
        'Email': SES_RECEIVER_EMAIL
    }

    send_message(data)
    response = lambda_handler(None, None)
    print('Response:', response)