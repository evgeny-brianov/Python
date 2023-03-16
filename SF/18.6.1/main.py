import telebot
import conf as cfg
from extensions import ConvException, Exchange

bot = telebot.TeleBot(cfg.TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'Привет {message.from_user.first_name}! Я Меняла-бот и я знаю толк в денежках! \
    \n- напомнить, что я могу через команду /help. \
    \n- список доступных валют через команду /values.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = f'Для конвертации, напиши команду такого формата, используя пробелы:' \
           f'\n <имя валюты1> <имя валюты2> <количество>' \
           f"\n Например: рубль доллар 1"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in cfg.currency.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvException('Введите команду или 3 параметра. \nНапример: рубль доллар 1')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ConvException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()