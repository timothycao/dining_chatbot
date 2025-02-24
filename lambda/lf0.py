import json
from lex.send import send_to_lex

def lambda_handler(event, context):
    # Extract the user message from the API request
    body = json.loads(event['body'])
    user_message = body.get('message', '')
    user_id = body.get('user_id', 'default')

    # Send user message to Lex
    lex_response = send_to_lex(user_id, user_message)

    # Check if Lex responded successfully
    if lex_response and 'messages' in lex_response:
        # Extract Lex's response message(s) as an array
        response_message = [message['content'] for message in lex_response['messages']]
        
        # Return Lex's response as API response
        return {'statusCode': 200, 'body': json.dumps({'response': response_message})}
    else:
        # Return an error response if Lex didn't respond
        return {'statusCode': 500, 'body': json.dumps({'error': 'Failed to get response from Lex'})}

# Testing
if __name__ == '__main__':
    event = {
        'body': json.dumps({
            'userId': 'user-123',
            'message': 'I need some restaurant suggestions'
        })
    }
    response = lambda_handler(event, None)
    print('Response:', json.loads(response['body']))