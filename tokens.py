import requests
from database import *

def count_tokens(text):
    """Count the number of tokens in the given text using Yandex API."""
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize'
    headers = {
        'Authorization': f'Bearer {iam}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f'gpt://{folder}/yandexgpt/latest',
        'maxTokens': MAX_GPT_TOKENS,
        'text': text
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return len(response.json()['tokens'])
    except Exception as e:
        logging.error(f"Error counting tokens: {e}")
        return 0

def check_tokens_data(user_id, param):
    """Retrieve token or session data for the user."""
    return get_user_tokens_data(user_id, param)

def start_session(user_id):
    """Start a new session for the user, decrementing session count."""
    current_sessions = check_tokens_data(user_id, 'sessions')
    update_sessions(user_id, current_sessions[0][0] - 1)

def cut_tokens(user_id, response):
    """Deduct tokens used in the response from the user's balance."""
    tokens = count_tokens(response)
    update_tokens(user_id, tokens)
    logging.info(f"User {get_username(user_id)} deducted {tokens} tokens")
