import json
from lex.send import send_to_lex

def lambda_handler(event, context):
    # Extract the user message from the API request
    user_id, user_message = 'default', ''

    # Standard request format
    if 'user_id' in event and 'message' in event:
        user_id = event.get('user_id', 'default')
        user_message = event.get('message', '')
    
    # Frontend request format
    if 'messages' in event:
        user_message = event['messages'][0]['unstructured']['text']

    # Send user message to Lex
    lex_response = send_to_lex(user_id, user_message)

    # Check if Lex responded successfully
    if lex_response and 'messages' in lex_response:
        # Frontend response format
        response_messages = [
            {
                'type': 'unstructured',
                'unstructured': {
                    'text': message['content']
                }
            }
            for message in lex_response['messages']
        ]

        # Return Lex's response as API response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'messages': response_messages
        }
    else:
        # Return an error response if Lex didn't respond
        return {'statusCode': 500, 'body': {'error': 'Failed to get response from Lex'}}

# Testing
if __name__ == '__main__':
    event = {
        'messages': [
            {
                'type': 'unstructured',
                'unstructured': {
                    'text': 'I need some restaurant suggestions'
                }
            }
        ]
    }
    response = lambda_handler(event, None)
    print('Response:', response)