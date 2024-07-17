import requests
from database import *
from tokens import cut_tokens
from info import *



def post_request(messages):
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

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        text = response.json()['result']['alternatives'][0]['message']['text']
        return text
    else:
        error_message = response.text
        logging.error(f'Ошибка GPT - {error_message}')
        return False


SYSTEM_PROMPT = (
    'Ты постепенно пишешь историю. Если человек просит, продолжаешь уже написанное. '
    'Если это уместно, ты можешь добавлять в историю диалог между персонажами. '
    'Диалоги пиши с новой строки и отделяй тире. '
    'Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю.'
)
START_STORY = '\nНапиши начало истории. Не пиши никакой пояснительный текст от себя'
CONTINUE_STORY = '\nПродолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = '\nНапиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'


def create_system_prompt(user_id):
    prompt = SYSTEM_PROMPT
    user_data = get_story_settings(user_id)
    prompt += (f'\nНПиши историю в стиле {user_data[0][0]} с главным героем {user_data[0][1]}. '
               f'Вот начальная локация: \n{user_data[0][2]}.\n')
    if user_data[0][3]:
        prompt += f'Также пользователь попросил учесть следующую дополнительную информацию: {user_data[0][3]} '
    prompt += 'Не пиши никакие подсказки пользователю, что делать дальше. Он сам знает'
    return prompt


def ask_gpt(user_id, mode):
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

