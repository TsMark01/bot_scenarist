from telebot.types import ReplyKeyboardMarkup
import telebot
from telebot import TeleBot
from buttons import *
import logging
from gpt import *
from tokens import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)
bot = TeleBot(tg)
user_data = {}

@bot.message_handler(commands=['debug'])
def debug(message):
    with open('errors.cod.log', 'rb') as file:
        bot.send_document(message.chat.id, file)
def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info('Пользователь нажал старт')
    if add_user(user_id, message.from_user.username):
        bot.send_message(message.chat.id,f'Привет, {user_name}!Я Кристофер Нолан, один из лучших сценаристов мира.\n'
                         f' Ты наверное знаешь фильм Интерстеллар или Оппенгеймер, я сценарист в этих фильмах.\n'
                         f'Чтобы взаимодействовать со мной нажимай на /story', reply_markup=markup_help)

    else:
        bot.send_message(message.chat.id, 'Извини, но на данный момент все свободные места для пользователей заняты :( '
                                          'Попробуй снова через некоторое время', reply_markup=hideKeyboard)
        logging.warning('Достигнут лимит пользователей бота')



@bot.message_handler(commands=['help'])
def handle_help(message):
    logging.info('Пользователь нажал хелп')
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if add_user(user_id, user_name):
        bot.send_message(message.chat.id,
                         "Для начала написания истории воспользуйтесь командой /story. Далее выберите жанр истории, главного персонажа и место действия. Возможно также добавить дополнительные сведения, такие как время событий или другие детали, необходимые читателю. После этого активируйте /begin, и нейросеть приступит к созданию начала вашей истории.После этого начнется ваша сессия работы с нейросетью. У каждого пользователя есть ограниченное количество сессий, и в каждой из них имеется лимит токенов. Не беспокойтесь, бот предупредит вас о том, когда токены закончатся, и вам будет возможность завершить историю. Проинформироваться о своем балансе можно с помощью /tokens.По завершении каждого отрывка истории можно запросить у нейросети продолжение рассказа (/continue) или завершить его (/end). По завершении сессии будет доступен результат с помощью /wholestory, reply_markup=markup_help",
                         reply_markup=markup_help)


    else:
        bot.send_message(message.chat.id, 'Извини, но на данный момент все свободные места для пользователей заняты :( '
                                          'Попробуй снова через некоторое время', reply_markup=hideKeyboard)
        logging.warning('Достигнут лимит пользователей бота')


@bot.message_handler(commands=['story'])
def start_new_story(message):
    logging.info('Пользователь нажал стори')

    user_id = message.from_user.id

    current_sessions = int(check_tokens_data(user_id, 'sessions')[0][0])
    if add_user(user_id, message.from_user.username):
        if current_sessions > 0:
            start_story(user_id)

        if current_sessions < 1:
            bot.send_message(message.chat.id, 'К сожалению, у тебя закончились все сессии!',
                             reply_markup=hideKeyboard)
            logging.warning(f'У пользователя {get_username(message.chat.id)} закончились сессии')
        else:
            if current_sessions < 2:
                bot.send_message(message.chat.id, 'Предупреждаем, у тебя осталась только одна сессия. Используй её '
                                                  'правильно!')

            bot.send_message(message.chat.id, "Выбери жанр", reply_markup=markup_genre)

    else:
        bot.send_message(message.chat.id, 'Извини, но на данный момент все свободные места для пользователей заняты :( '
                                          'Попробуй снова через некоторое время', reply_markup=hideKeyboard)
        logging.warning('Достигнут лимит пользователей бота')

@bot.message_handler(commands=['begin'])
def start_writing_story(message):
    logging.info('Пользователь нажал бегин')
    user_id = message.from_user.id
    check_tokens = check_tokens_data(user_id, 'tokens')[0]
    if check_tokens[0] > 0:
        start_session(user_id)
        logging.info(f'Пользователь {get_username(user_id)} запросил начало истории')
        story_params = get_story_settings(user_id)[0]
        bot.send_message(message.chat.id, f'Итак,\nжанр - {story_params[0]}\nглавный герой - {story_params[1]}\nместо '
                                          f'действия - {story_params[2]}\nдополнительная информация - {story_params[3]}'
                                          '\n\nПрекрасный выбор! Нейросеть уже начинает генерировать...')
        res = ask_gpt(user_id, mode='start')
        bot.send_message(message.chat.id, res,
                         reply_markup=create_keyboard(['/continue', '/end']))
    else:
        bot.send_message(message.chat.id, 'К сожалению, у тебя закончились все сессии!',
                         reply_markup=hideKeyboard)

@bot.message_handler(commands=['continue'])
def continue_story(message):
    logging.info('Пользователь нажал продолжить')
    user_id = message.from_user.id
    check = check_tokens_data(user_id, 'tokens')[0]
    if check[0] < MAX_GPT_TOKENS * 3:
        res = ask_gpt(user_id, mode='continue')
        bot.send_message(message.chat.id, res)
        bot.send_message(message.chat.id, 'В этой сессии осталось совсем немного токенов! Пора заканчивать историю',
                         reply_markup=create_keyboard(['/end']))
    else:
        bot.send_message(message.chat.id, ask_gpt(user_id, mode='continue'),
                         reply_markup=create_keyboard(['/continue', '/end']))


@bot.message_handler(commands=['end'])
def finish_story(message):
    logging.info('Пользователь нажал завершить')
    user_id = message.from_user.id
    bot.send_message(message.chat.id, ask_gpt(user_id, mode='end'),
                     reply_markup=create_keyboard(['/wholestory', '/tokens', '/story']))


@bot.message_handler(commands=['wholestory'])
def send_whole_story(message):
    logging.info('Пользователь нажал отослать всю историю')
    user_id = message.from_user.id
    story = get_story_history(user_id)[0][0]
    try:
        if len(story) < 4096:
            bot.send_message(message.chat.id, story, reply_markup=create_keyboard(['/tokens', '/story']))
        else:
            for i in range(len(story) // 4096 + 1):
                bot.send_message(message.chat.id, story[4096*i:4096*(i+1)],
                                 reply_markup=create_keyboard(['/tokens', '/story']))
            logging.warning('Слишком длинная целая история')
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, 'Произошла непредвиденная ситуация. Возможно, твоя история получилась '
                                          'слишком длинной для Telegram. Попробуй повторить попытку позже',
                         reply_markup=create_keyboard(['/tokens', '/newstory']))

@bot.message_handler(commands=['tokens'])
def send_tokens_info(message):
    logging.info('Пользователь нажал токенс')
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        tok = check_tokens_data(user_id, 'tokens')
        bot.send_message(message.chat.id, f'У тебя осталось сессий: {check_tokens_data(message.chat.id, "sessions")}\n'
                                          'На последнюю историю ты потратил токенов: '
                                          f'{MAX_TOKENS_IN_SESSION - tok[0][0]}',
                         reply_markup=create_keyboard(['/story']))
    else:
        bot.send_message(message.chat.id, 'Извини, но на данный момент все свободные места для пользователей заняты :( '
                                          'Попробуй снова через некоторое время', reply_markup=hideKeyboard)
        logging.warning('Достигнут лимит пользователей бота')



@bot.message_handler(content_types=['text'])
def handle_message(message):
    user_id = message.from_user.id
    if message.text in genres:
        update_genre(message.text, user_id)
        bot.send_message(message.chat.id, 'Выбери главного героя',
                         reply_markup=markup_characters)
    elif message.text in main_characters:
        update_characters(message.text, user_id)
        bot.send_message(message.chat.id, 'Где будет происходить сцена', reply_markup=markup_settings)
    elif message.text in settings:
        update_setting(message.text, user_id)
        bot.send_message(message.chat.id,  'Теперь ты можешь добавить от себя уточнения.')
    elif message.text:
        update_info(message.text, user_id)
        bot.send_message(message.chat.id, 'Жми на /begin', reply_markup=create_keyboard(['/begin']))
    else:
        bot.send_message(message.chat.id,
                         'Тебе следует воспользоваться командой или кнопкой, другого бот не понимает :(',
                         reply_markup=hideKeyboard())


bot.polling()