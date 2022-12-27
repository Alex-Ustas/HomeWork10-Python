import telebot
import bot_api
import requests as rq
import xmltodict as xml

# Name: AlexCurrencyRate
# Bot name: currency_rate_hw10_bot

bot = telebot.TeleBot(bot_api.TOKEN)
description = """
Предоставляет информацию о текущем
курсе валют из *Центробанка*.
Необходимо сделать запрос в виде
[/usd] - курс *доллара*
[/eur] - курс *евро*
[/cny] - курс *юаня*
и так далее."""


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    bot.send_message(message.chat.id, description, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def get_currency(message):
    s = rq.get('http://www.cbr.ru/scripts/XML_daily.asp')
    dct = xml.parse(s.text)['ValCurs']['Valute']
    curr = message.text[1:].upper()
    if len(curr) == 3 and message.text[0] == '/':
        for val in dct:
            if val['CharCode'] == curr:
                rate = float(val["Value"].replace(',', '.')) / int(val["Nominal"])
                bot.send_message(message.chat.id,
                                 f'Курс валюты {curr} на текущий день: \n{val["Name"]} - {rate}')
                break
        else:
            bot.reply_to(message, 'Валюта не определена')
    else:
        bot.reply_to(message, 'Неверный ввод.\nСправка - /help')


bot.polling()
