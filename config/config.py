import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Gateway
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

ENDPOINTS = {
    'chatbot': f'{API_GATEWAY_URL}/chatbot'
}