from telebot import types
from info import *

genres = ['Comedy', 'Fantasy', 'Horror']
main_characters = ['Harry Potter', 'Black Widow', 'Captain Jack Sparrow']
settings = ['Megapolis', 'Village', 'Dark Forest']

markup_ec = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
markup_ec.add("/continue", "/end")

hideKeyboard = types.ReplyKeyboardRemove()

markup_menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markup_menu.add("/help", "/story")

markup_help = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markup_help.add("/tokens", "/story")

markup_genre = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
for i in genres:
    markup_genre.add(i)

markup_characters = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
for i in main_characters:
    markup_characters.add(i)

markup_settings = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
for i in settings:
    markup_settings.add(i)

markup_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
markup_start.add("/generate")

markup_generate = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
markup_generate.add('End')

markup_limit = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
markup_limit.add("/tokens", "/help")
