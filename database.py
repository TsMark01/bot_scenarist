import logging
import sqlite3
from info import *

def open_db():
    """Open a connection to the SQLite database."""
    con = sqlite3.connect('db.hope', check_same_thread=False)
    cur = con.cursor()
    return con, cur

def create_tables():
    """Create necessary tables in the database if they don't exist."""
    connection, cursor = open_db()

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL UNIQUE,
        tg_username TEXT NOT NULL,
        sessions INTEGER DEFAULT {MAX_SESSIONS},
        tokens INTEGER DEFAULT {MAX_TOKENS_IN_SESSION}
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER NOT NULL,
        genre TEXT,
        main_character TEXT,
        setting TEXT,
        info TEXT,
        history TEXT DEFAULT "",
        title TEXT,
        FOREIGN KEY (author_id) REFERENCES users (id)
    );
    ''')

    cursor.close()
    connection.commit()
    connection.close()

    logging.info('Tables created')

def change_db(sql, params=()):
    """Execute a change query on the database."""
    connection, cursor = open_db()
    cursor.execute(sql, params)
    cursor.close()
    connection.commit()
    connection.close()

def get_from_db(sql, params=()):
    """Retrieve data from the database."""
    connection, cursor = open_db()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def user_in_db(user_id):
    """Check if a user exists in the database."""
    res = get_from_db(f'SELECT * FROM users WHERE chat_id = {user_id};')
    return res

def add_user(user_id, username):
    """Add a new user to the database if slots are available."""
    if not user_in_db(user_id):
        if len(get_from_db('SELECT * FROM users')) < MAX_USERS:
            change_db(
                'INSERT INTO users (chat_id, tg_username, sessions, tokens) VALUES (?, ?, ?, ?);',
                (user_id, username, MAX_SESSIONS, MAX_TOKENS_IN_SESSION)
            )
            logging.info(f'Added user {get_username(user_id)}')
        else:
            logging.warning(f'Database already has {MAX_USERS} users')
            return False
    return True

def get_username(user_id):
    """Get the username for a given user ID."""
    return get_from_db(f'SELECT tg_username FROM users WHERE chat_id = {user_id};')

def start_story(user_id):
    """Start a new story entry for the user."""
    change_db(
        'INSERT INTO stories (author_id) VALUES ((SELECT id FROM users WHERE chat_id = ?));',
        (user_id,)
    )

def set_param(param, value, user_id):
    """Set a parameter for the current story."""
    change_db(
        f"UPDATE stories SET {param} = ? WHERE author_id = (SELECT id FROM users WHERE chat_id = ?) AND history = '';",
        (value, user_id)
    )

def update_genre(genre, user_id):
    """Update the genre for the user's story."""
    change_db(
        f"UPDATE stories SET genre = '{genre}' WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id});"
    )

def update_characters(characters, user_id):
    """Update the main character for the user's story."""
    change_db(
        f"UPDATE stories SET main_character = '{characters}' WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id});"
    )

def update_setting(sett, user_id):
    """Update the setting for the user's story."""
    change_db(
        f"UPDATE stories SET setting = '{sett}' WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id});"
    )

def update_info(inf, user_id):
    """Update additional info for the user's story."""
    change_db(
        f"UPDATE stories SET info = '{inf}' WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id});"
    )

def get_story_settings(user_id):
    """Get the story settings for the user."""
    return get_from_db(
        f'SELECT genre, main_character, setting, info FROM stories '
        f'WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id}) '
        f'ORDER BY id DESC LIMIT 1;'
    )

def get_story_history(user_id):
    """Get the story history for the user."""
    return get_from_db(
        f'SELECT history FROM stories '
        f'WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id}) '
        f'ORDER BY id DESC LIMIT 1;'
    )

def update_history(user_id, new_answer):
    """Update the story history with new content."""
    current_history = get_story_history(user_id)[0][0]
    change_db(
        f'UPDATE stories SET history = "{current_history + " " + new_answer}" '
        f'WHERE id = (SELECT MAX(id) FROM stories '
        f'WHERE author_id = (SELECT id FROM users WHERE chat_id = {user_id}));'
    )
    logging.info(f'Added new story fragment for user {get_username(user_id)}:\n{new_answer}')

def get_user_tokens_data(user_id, param):
    """Get token or session data for the user."""
    result = get_from_db(f'SELECT {param} FROM users WHERE chat_id = {user_id};')
    return result

def update_sessions(user_id, sessions):
    """Update the number of sessions for the user."""
    change_db(f'UPDATE users SET sessions = {sessions}, tokens = {MAX_TOKENS_IN_SESSION} WHERE chat_id = {user_id};')

def update_tokens(user_id, tokens):
    """Update the token count for the user."""
    user_tok = get_user_tokens_data(user_id, "tokens")[0][0]
    result = user_tok - tokens
    change_db(f'UPDATE users SET tokens = {result} WHERE chat_id = {user_id};')

create_tables()
