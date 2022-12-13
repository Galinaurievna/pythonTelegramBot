import telebot
from config import keys, TOKEN
from extensions import APIException, ValueConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в виде: \n  <имя валюты, цену которой нужно узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException(f"Слишком много параметров")
        quote, base, amount = values
        total_base = ValueConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать комманду\n{e}")
    else:
        amount = int(amount)
        if amount >= 1:
            total_base = str(float(amount * total_base))
        text = f"цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling()