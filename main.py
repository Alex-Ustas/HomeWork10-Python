import telebot
import bot_api

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


@bot.message_handler(commands=['start'])
def game_help(message):
    bot.send_message(message.chat.id, description, parse_mode='Markdown')


bot.polling()
