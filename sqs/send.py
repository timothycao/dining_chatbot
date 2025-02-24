import json
import boto3
from config.config import SQS_QUEUE_URL

# Initialize SQS Client
sqs_client = boto3.client('sqs')

def send_to_sqs(data):
    try:
        response = sqs_client.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(data))
        # print(f'SQS response: {response}')
        return response
    except Exception as e:
        print(f'Error sending message to SQS: {e}')
        return None

# Testing
if __name__ == '__main__':
    data = {
        'Location': 'New York',
        'Cuisine': 'Italian',
        'PartySize': '2',
        'DiningTime': '7:00 PM',
        'Email': 'user@example.com'
    }
    response = send_to_sqs(data)
    print(response)