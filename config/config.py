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

# Yelp
YELP_API_URL = os.getenv('YELP_API_URL')
YELP_API_KEY = os.getenv('YELP_API_KEY')

# DynamoDB
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# OpenSearch
OPENSEARCH_URL = os.getenv('OPENSEARCH_URL')
OPENSEARCH_HEADERS = {'Content-Type': 'application/json'}
OPENSEARCH_AUTH = (os.getenv('OPENSEARCH_USERNAME'), os.getenv('OPENSEARCH_PASSWORD'))

# SES
SES_SENDER_EMAIL = os.getenv('SES_SENDER_EMAIL')
SES_RECEIVER_EMAIL = os.getenv('SES_RECEIVER_EMAIL')    # for testing