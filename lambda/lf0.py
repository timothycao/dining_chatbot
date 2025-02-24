import json

def lambda_handler(event, context):    
    return {
        'statusCode': 200,
        'body': json.dumps("I'm still under development. Please come back later.")
    }

# Testing
if __name__ == '__main__':
    response = lambda_handler(None, None)
    print('Response:', json.loads(response['body']))