import telebot
import bot_api
import requests as rq
import xmltodict as xml
from bs4 import BeautifulSoup as bs

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
и так далее.
Справка по криптовалюте:
[/bitcoin]"""


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    bot.send_message(message.chat.id, description, parse_mode='Markdown')


@bot.message_handler(commands=['bitcoin'])
def get_bitcoin(message):
    link = 'https://www.rbc.ru/crypto/currency/btcusd'
    res = rq.get(link)
    soup = bs(res.text, 'html.parser')
    content = soup.find('div', class_='chart__subtitle js-chart-value')
    bitcoin = content.next.strip() + ' BTC/USD'
    last_update = soup.find('div', class_='chart__description')
    now = last_update.find('span').next
    bot.send_message(message.chat.id,
                     f'*{bitcoin}*\nПоследнее обновление: {now}\
                     \nВзято с [РБК](https://www.rbc.ru/crypto/currency/btcusd)',
                     parse_mode='Markdown')


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
