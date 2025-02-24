import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Gateway
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

ENDPOINTS = {
    'chatbot': f'{API_GATEWAY_URL}/chatbot'
}

# SQS
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Lex
LEX_BOT_ID = os.getenv('LEX_BOT_ID')
LEX_BOT_ALIAS_ID = os.getenv('LEX_BOT_ALIAS_ID')
LEX_LOCALE_ID = os.getenv('LEX_LOCALE_ID')