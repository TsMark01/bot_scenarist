import requests
from database import *
from tokens import cut_tokens
from info import *

def post_request(messages):
    """Send a POST request to Yandex GPT for completion."""
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        'Authorization': f'Bearer {iam}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f'gpt://{folder}/yandexgpt-lite',
        'completionOptions': {
            'stream': False,
            'temperature': 0.6,
            'maxTokens': MAX_GPT_TOKENS
        },
        'messages': messages
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            text = response.json()['result']['alternatives'][0]['message']['text']
            return text
        else:
            error_message = response.text
            logging.error(f'GPT error - {error_message}')
            return False
    except Exception as e:
        logging.error(f"Error in GPT request: {e}")
        return False

SYSTEM_PROMPT = (
    "You gradually write the story. If the person asks, continue the already written one. "
    "If appropriate, you can add dialogue between characters to the story. "
    "Write dialogues on a new line and separate with a dash. "
    "Do not write any explanatory text at the beginning, just logically continue the story."
)
START_STORY = '\nWrite the beginning of the story. Do not write any explanatory text from yourself.'
CONTINUE_STORY = '\nContinue the plot in 1-3 sentences and leave an intrigue. Do not write any explanatory text from yourself.'
END_STORY = '\nWrite the ending of the story with an unexpected twist. Do not write any explanatory text from yourself.'

def create_system_prompt(user_id):
    """Create a system prompt based on user story settings."""
    prompt = SYSTEM_PROMPT
    user_data = get_story_settings(user_id)
    prompt += (
        f'\nWrite the story in the style of {user_data[0][0]} with the main character {user_data[0][1]}. '
        f'Here is the initial location: \n{user_data[0][2]}.\n'
    )
    if user_data[0][3]:
        prompt += f'Also, the user asked to consider the following additional information: {user_data[0][3]} '
    prompt += 'Do not write any hints to the user on what to do next. They know themselves.'
    return prompt

def ask_gpt(user_id, mode):
    """Ask Yandex GPT to generate story text based on mode."""
    system_prompt = create_system_prompt(user_id)
    messages = []
    if mode == 'start':
        messages = [{'role': 'user', 'text': system_prompt + START_STORY}]
    elif mode == 'continue':
        messages = [{'role': 'user', 'text': system_prompt + CONTINUE_STORY}]
        assistant_prompt = get_story_history(user_id)[-1][0]
        messages.append({'role': 'assistant', 'text': assistant_prompt})
    elif mode == 'end':
        messages = [{'role': 'user', 'text': system_prompt + END_STORY}]
        assistant_prompt = get_story_history(user_id)[-1][0]
        messages.append({'role': 'assistant', 'text': assistant_prompt})
    answer = post_request(messages)
    if answer:
        update_history(user_id, answer)
        cut_tokens(user_id, answer)
    else:
        answer = ''
    return answer

