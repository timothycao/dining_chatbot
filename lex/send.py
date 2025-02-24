import boto3
from config.config import LEX_BOT_ID, LEX_BOT_ALIAS_ID, LEX_LOCALE_ID

# Initialize Lex Client
lex_client = boto3.client('lexv2-runtime')

def send_to_lex(user_id, text_message):
    try:
        response = lex_client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId=LEX_LOCALE_ID,
            sessionId=user_id,
            text=text_message
        )
        # print(f'Lex Response: {response}')
        return response
    except Exception as e:
        print(f'Error sending message to Lex: {e}')
        return None

# Testing
if __name__ == '__main__':
    user_id = 'user-123'
    message = 'I need some restaurant suggestions'
    response = send_to_lex(user_id, message)
    print(response['messages'])