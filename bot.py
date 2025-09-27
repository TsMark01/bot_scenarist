import telebot
from telebot import types
import logging
from buttons import *
from gpt import *
from tokens import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)
bot = telebot.TeleBot(tg)
user_data = {}

@bot.message_handler(commands=['debug'])
def debug(message):
    """Send the error log file to the user."""
    try:
        with open('errors.cod.log', 'rb') as file:
            bot.send_document(message.chat.id, file)
        logging.info("Debug log sent successfully")
    except Exception as e:
        bot.send_message(message.chat.id, "Failed to send debug log. Please try again later.")
        logging.error(f"Error sending debug log: {e}")

def create_keyboard(buttons_list):
    """Create a reply keyboard with the given buttons."""
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Handle the /start command and welcome the user."""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info("User started the bot")
    if add_user(user_id, message.from_user.username):
        bot.send_message(
            message.chat.id,
            f"Hello, {user_name}! I'm Christopher Nolan, one of the world's best screenwriters.\n"
            f"You probably know films like Interstellar or Oppenheimer—I'm the screenwriter for those.\n"
            f"To interact with me, use /story.",
            reply_markup=markup_help
        )
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['help'])
def handle_help(message):
    """Handle the /help command and provide usage instructions."""
    logging.info("User requested help")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if add_user(user_id, user_name):
        bot.send_message(
            message.chat.id,
            "To start writing a story, use /story. Then select the genre, main character, and setting. "
            "You can also add additional details like time period or other elements. "
            "After that, use /begin, and the AI will start creating the beginning of your story. "
            "This will begin your session with the AI. Each user has a limited number of sessions, "
            "and each session has a token limit. Don't worry—the bot will notify you when tokens are low, "
            "and you'll have a chance to finish the story. Check your balance with /tokens. "
            "After each story fragment, you can request the next part with /continue, end the story with /end, "
            "or view the full story with /wholestory.",
            reply_markup=markup_help
        )
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['story', 'newstory'])
def handle_story(message):
    """Handle the /story or /newstory command to start a new story."""
    logging.info("User started a new story")
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        start_session(user_id)
        bot.send_message(message.chat.id, "Choose a genre:", reply_markup=markup_genre)
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['begin'])
def handle_begin(message):
    """Handle the /begin command to generate the story beginning."""
    logging.info("User began story generation")
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        if check_tokens_data(user_id, 'tokens')[0][0] > 0:
            answer = ask_gpt(user_id, 'start')
            bot.send_message(message.chat.id, answer, reply_markup=markup_ec)
        else:
            bot.send_message(
                message.chat.id,
                "Sorry, you've run out of tokens for this session :(",
                reply_markup=create_keyboard(['/tokens', '/story'])
            )
            logging.warning("User out of tokens")
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['continue'])
def handle_continue(message):
    """Handle the /continue command to continue the story."""
    logging.info("User continued the story")
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        if check_tokens_data(user_id, 'tokens')[0][0] > 0:
            answer = ask_gpt(user_id, 'continue')
            bot.send_message(message.chat.id, answer, reply_markup=markup_ec)
        else:
            bot.send_message(
                message.chat.id,
                "Sorry, you've run out of tokens for this session :(",
                reply_markup=create_keyboard(['/tokens', '/story'])
            )
            logging.warning("User out of tokens")
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['end'])
def handle_end(message):
    """Handle the /end command to end the story."""
    logging.info("User ended the story")
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        if check_tokens_data(user_id, 'tokens')[0][0] > 0:
            answer = ask_gpt(user_id, 'end')
            bot.send_message(message.chat.id, answer, reply_markup=create_keyboard(['/wholestory', '/story']))
        else:
            bot.send_message(
                message.chat.id,
                "Sorry, you've run out of tokens for this session :(",
                reply_markup=create_keyboard(['/tokens', '/story'])
            )
            logging.warning("User out of tokens")
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['wholestory'])
def handle_wholestory(message):
    """Handle the /wholestory command to view the full story."""
    logging.info("User requested full story")
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        try:
            story = get_story_history(user_id)[0][0]
            if len(story) > 4096:
                for i in range(len(story) // 4096 + 1):
                    bot.send_message(
                        message.chat.id,
                        story[4096 * i : 4096 * (i + 1)],
                        reply_markup=create_keyboard(['/tokens', '/story'])
                    )
                logging.warning("Full story is too long")
            else:
                bot.send_message(message.chat.id, story, reply_markup=create_keyboard(['/tokens', '/story']))
        except telebot.apihelper.ApiTelegramException:
            bot.send_message(
                message.chat.id,
                "An unexpected error occurred. Your story might be too long for Telegram. Please try again later.",
                reply_markup=create_keyboard(['/tokens', '/story'])
            )
            logging.error("Error sending full story")
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(commands=['tokens'])
def send_tokens_info(message):
    """Handle the /tokens command to show token and session info."""
    logging.info("User requested token info")
    user_id = message.from_user.id
    if add_user(user_id, message.from_user.username):
        tok = check_tokens_data(user_id, 'tokens')
        bot.send_message(
            message.chat.id,
            f"You have {check_tokens_data(message.chat.id, 'sessions')[0][0]} sessions left.\n"
            f"For the last story, you spent {MAX_TOKENS_IN_SESSION - tok[0][0]} tokens.",
            reply_markup=create_keyboard(['/story'])
        )
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, but all user slots are currently full :( Please try again later.",
            reply_markup=hideKeyboard
        )
        logging.warning("User limit reached")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    """Handle text messages for story settings."""
    user_id = message.from_user.id
    if message.text in genres:
        update_genre(message.text, user_id)
        bot.send_message(message.chat.id, "Choose the main character:", reply_markup=markup_characters)
    elif message.text in main_characters:
        update_characters(message.text, user_id)
        bot.send_message(message.chat.id, "Where will the scene take place?", reply_markup=markup_settings)
    elif message.text in settings:
        update_setting(message.text, user_id)
        bot.send_message(message.chat.id, "Now you can add your own clarifications.")
    elif message.text:
        update_info(message.text, user_id)
        bot.send_message(message.chat.id, "Press /begin", reply_markup=create_keyboard(['/begin']))
    else:
        bot.send_message(
            message.chat.id,
            "Please use a command or button—the bot doesn't understand anything else :(",
            reply_markup=hideKeyboard
        )

bot.polling()
