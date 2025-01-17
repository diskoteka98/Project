import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot("6562006546:AAHvjx7VznjR7CbyKUtwaHWJbTKX-Yzwpa0")
c = CurrencyConverter()
amount = 0


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,  "Привет! Веведите сумму")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Впишите сумму")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
        btn4 = types.InlineKeyboardButton("Другое значение", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,"Выберите пару валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше 0. Впишите сумму")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        value = call.data.upper().split("/")
        res = c.convert(amount, value[0], value[1])
        bot.send_message(call.message.chat.id, f"Получается: {round(res, 2)}. Можете занова ввести сумму")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через слэш")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        value = message.text.upper().split("/")
        res = c.convert(amount, value[0], value[1])
        bot.send_message(message.chat.id, f"Получается: {round(res, 2)}. Можете занова ввести сумму")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "Что-то не так. Впишите значение заново")
        bot.register_next_step_handler(message, my_currency)


bot.polling(non_stop=True)