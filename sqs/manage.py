import json
import boto3
from config.config import SQS_QUEUE_URL, SES_RECEIVER_EMAIL

# Initialize SQS Client
sqs_client = boto3.client('sqs')

def send_message(data):
    try:
        response = sqs_client.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(data))
        return response
    except Exception as e:
        print(f'Error sending message to SQS: {e}')
        return None

def receive_message():
    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=2
        )
        messages = response.get('Messages', [])
        return messages[0] if messages else None
    except Exception as e:
        print(f'Error receiving message from SQS: {e}')
        return None

def delete_message(receipt_handle):
    try:
        sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
    except Exception as e:
        print(f'Error deleting message from SQS: {e}')
        return None

# Testing
if __name__ == '__main__':
    data = {
        'Location': 'New York',
        'Cuisine': 'Italian',
        'PartySize': '2',
        'DiningTime': '7:00 PM',
        'Email': SES_RECEIVER_EMAIL
    }

    response = send_message(data)
    print('Send message response:', response)

    message = receive_message()
    print('Received message:', message)

    # response = delete_message(message['ReceiptHandle'])
    # print('Delete message response:', response)