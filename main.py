
import telebot
import wikipedia
from wikipedia import PageError
import geonamescache
import time
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
print(TOKEN)

bot = telebot.TeleBot(TOKEN)

gc = geonamescache.GeonamesCache()


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я бот который умеет давать статьи о городах'
    )

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Назови любой город и я расскажу о нем'
    )



@bot.message_handler(content_types=['text'])
def message_handler(message):
    wikipedia.set_lang('ru')
    user_city = message.text
    city = wikipedia.search(user_city)


    try:
        page_of_city = wikipedia.page(user_city)
        city_for_location = gc.search_cities(user_city)
        info_text = wikipedia.summary(city[0], sentences=30)


        if city:
            bot.send_message(message.chat.id, f'👌Отлично! Такой город существует')
            bot.send_message(message.chat.id, f'{info_text}')
            if city_for_location:
                lat = city_for_location[0].get('latitude')
                lon = city_for_location[0].get('longitude')
                bot.send_location(message.chat.id, lat, lon)
                if page_of_city.images[0]:
                    bot.send_photo(message.chat.id, page_of_city.images[0])
                else:
                    bot.send_message(message.chat.id, 'К сожалению, фото для выбранного города не найдено')
            bot.send_message(message.chat.id, 'Называй следующий город🌆')
        else:
            bot.send_message(message.chat.id, 'Такой город не найден😥. Назавите другой город')



    except wikipedia.exceptions.PageError:
        bot.send_message(message.chat.id, 'Такой город не найден😥. Назавите другой город')


bot.polling(none_stop=True)