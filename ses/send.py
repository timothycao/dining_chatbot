import json
import boto3
from config.config import SES_SENDER_EMAIL

# Initialize SES Client
ses_client = boto3.client('ses')

def send_email(recipient_email, restaurants, cuisine, location):
    subject = 'Restaurant Recommendations'

    if restaurants:
        body = f'Hello! Here are my {cuisine} restaurant recommendations in {location}:\n\n'
        for i, restaurant in enumerate(restaurants):
            body += f'{i + 1}. {restaurant.get('name', 'N/A')}, located at {restaurant.get('address', 'N/A')}\n'
        body += '\nEnjoy your meal!'
    else:
        body = f"Hello! Unfortunately, I couldn't find any {cuisine} restaurants in {location}."

    response = ses_client.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}},
        },
    )

    print(f'Email sent to {recipient_email}: {json.dumps(response, indent=2)}')