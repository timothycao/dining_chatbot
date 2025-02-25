import json
import boto3
from config.config import SES_SENDER_EMAIL

# Initialize SES Client
ses_client = boto3.client('ses')

def send_email(recipient_email, restaurant):
    subject = 'Restaurant Recommendations'
    body = f"""
    Hello! Here are my restaurant recommendations:

    Restaurant: {restaurant.get('name', 'N/A')}
    Address: {restaurant.get('address', 'N/A')}

    Enjoy your meal!
    """

    response = ses_client.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}},
        },
    )

    print(f'Email sent to {recipient_email}: {json.dumps(response, indent=2)}')