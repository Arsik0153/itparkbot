import telebot
from telebot import types
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.43.53", username="robot", password="maker")
ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect("192.168.43.205", username="robot", password="maker")

global state
state = {}
bot = telebot.TeleBot("689225093:AAEaN6bjUnretqmUC_jQ4SxCirVOrR2grUM")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Пополнить баланс')
    itembtn2 = types.KeyboardButton('Зайти в аттракцион')
    itembtn3 = types.KeyboardButton('Баланс')
    itembtn4 = types. KeyboardButton('Купить продукт')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Добро пожаловать в ITLand!\n\nДля входа на аттракцион пополните ваш баланс.", reply_markup=markup)
    state[message.chat.id] = {"balance": 0, "step": 0}
    print(state)

@bot.message_handler(func=lambda message: message.text == 'Пополнить баланс')
def popupBalance(message):
    global state
    state[message.chat.id]["step"] = 1
    bot.send_message(message.chat.id, "Введите сумму")

@bot.message_handler(func=lambda message: message.text == 'Зайти в аттракцион')
def gotoAtt(message):
    global state
    state[message.chat.id]["step"] = 2
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Колесо обозрения. Цена: 690 тенге')
    itembtn2 = types.KeyboardButton('Детская карусель. Цена: 790 тенге')
    itembtn3 = types.KeyboardButton('Бумеранг. Цена: 800 тенге')
    itembtn4 = types.KeyboardButton('Цепочная карусель. Цена: 400 тенге')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Выберите аттракцион.", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == 'Купить продукт')
def gotoHav(message):
    global state
    state[message.chat.id]["step"] = 7
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Апельсин. Цена: 140 тенге')
    itembtn2 = types.KeyboardButton('Шоколадный батончик. Цена: 210 тенге')
    itembtn3 = types.KeyboardButton('Мороженое. Цена: 230 тенге')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Выберите продукт.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Баланс')
def getBalance(message):
    global state
    state[message.chat.id]["step"] = 0
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Пополнить баланс')
    itembtn2 = types.KeyboardButton('Зайти в аттракцион')
    itembtn3 = types.KeyboardButton('Баланс')
    itembtn4 = types.KeyboardButton('Купить продукт')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Ваш баланс: " + str(state[message.chat.id]["balance"]) + " тенге", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global state
    if state[message.chat.id]["step"] == 1:
        try:
            state[message.chat.id]["balance"] = state[message.chat.id]["balance"] + int(float(message.text))
            state[message.chat.id]["step"] = 0
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('Пополнить баланс')
            itembtn2 = types.KeyboardButton('Зайти в аттракцион')
            itembtn3 = types.KeyboardButton('Баланс')
            itembtn4 = types.KeyboardButton('Купить продукт')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            bot.send_message(message.chat.id, "Ваш баланс: " + str(state[message.chat.id]["balance"]) + " тенге", reply_markup=markup)
        except ValueError:
            bot.send_message(message.chat.id, "Только цифрами!")
    elif state[message.chat.id]["step"] == 2:
        useAtt(message)
    elif state[message.chat.id]["step"] == 7:
        useHav(message)
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понимаю. Пожалуйста, воспользуйтесь кнопками.")
    print(state)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global state
    if state[message.chat.id]["step"] == 0:
        try:
            state[message.chat.id]["balance"] = state[message.chat.id]["balance"] + int(float(message.text))
            state[message.chat.id]["step"] = 0
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('Пополнить баланс')
            itembtn2 = types.KeyboardButton('Зайти в аттракцион')
            itembtn3 = types.KeyboardButton('Баланс')
            itembtn4 = types.KeyboardButton('Купить продукт')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            bot.send_message(message.chat.id, "Ваш баланс: " + str(state[message.chat.id]["balance"]) + " тенге", reply_markup=markup)
        except ValueError:
            bot.send_message(message.chat.id, "Только цифрами!")
    elif state[message.chat.id]["step"] == 2:
        useAtt(message)
    elif state[message.chat.id]["step"] == 7:
        useHav(message)
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понимаю. Пожалуйста, воспользуйтесь кнопками.")
    print(state)

def useAtt(message):
    if message.text == "Детская карусель. Цена: 790 тенге":
        if not negativeBalance(message, 690):
            state[message.chat.id]["balance"] -= 690
            state[message.chat.id]["step"] = 0
            ssh2_stdin, ssh2_stdout, ssh2_stderr = ssh2.exec_command("pybricks-micropython main.py")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("pybricks-micropython main2.py")
    if message.text == "Колесо обозрения. Цена: 690 тенге":
        if not negativeBalance(message, 790):
            state[message.chat.id]["balance"] -= 790
            state[message.chat.id]["step"] = 0
            ssh2_stdin, ssh2_stdout, ssh2_stderr = ssh2.exec_command("pybricks-micropython main2.py")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("pybricks-micropython main.py")
    if message.text == "Бумеранг. Цена: 800 тенге":
        if not negativeBalance(message, 800):
            state[message.chat.id]["balance"] -= 800
            state[message.chat.id]["step"] = 0
            ssh2_stdin, ssh2_stdout, ssh2_stderr = ssh2.exec_command("pybricks-micropython main3.py")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("pybricks-micropython main3.py")
    if message.text == "Цепочная карусель. Цена: 400 тенге":
        if not negativeBalance(message, 400):
            state[message.chat.id]["balance"] -= 400
            state[message.chat.id]["step"] = 0
            ssh2_stdin, ssh2_stdout, ssh2_stderr = ssh2.exec_command("pybricks-micropython main4.py")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("pybricks-micropython main4.py")


    if state[message.chat.id]["step"] == 0:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Пополнить баланс')
        itembtn2 = types.KeyboardButton('Зайти в аттракцион')
        itembtn3 = types.KeyboardButton('Баланс')
        itembtn4 = types.KeyboardButton('Купить продукт')
        markup.add(itembtn1, itembtn2, itembtn3,itembtn4)
        bot.send_message(message.chat.id, "Вы зашли на аттракцион. У вас есть 1 минута чтобы занять своё место.\n\nПриятного отдыха!", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Пополнить баланс')
        itembtn2 = types.KeyboardButton('Зайти в аттракцион')
        itembtn3 = types.KeyboardButton('Баланс')
        itembtn4 = types.KeyboardButton('Купить продукт')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.send_message(message.chat.id, "У вас недостоточно баланса для входа на аттракцион. Пожалуйста, пополните баланс", reply_markup=markup)

def negativeBalance(message, price):
    if state[message.chat.id]["balance"] <= price:
        return True
    else:
        return False

def useHav(message):

    if message.text == "Апельсин. Цена: 140 тенге":
        if not negativeBalance(message, 140):
            state[message.chat.id]["balance"] -= 140
            state[message.chat.id]["step"] = 0

    if message.text == "Шоколадный батончик. Цена: 210 тенге":
        if not negativeBalance(message, 170):
            state[message.chat.id]["balance"] -= 170
            state[message.chat.id]["step"] = 0
    if message.text == "Мороженое. Цена: 230 тенге":
        if not negativeBalance(message, 230):
            state[message.chat.id]["balance"] -= 230
            state[message.chat.id]["step"] = 0

    if state[message.chat.id]["step"] == 0:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Пополнить баланс')
        itembtn2 = types.KeyboardButton('Зайти в аттракцион')
        itembtn3 = types.KeyboardButton('Баланс')
        itembtn4 = types.KeyboardButton('Купить продукт')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.send_message(message.chat.id, "Заберите продукт из ящика", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Пополнить баланс')
        itembtn2 = types.KeyboardButton('Зайти в аттракцион')
        itembtn3 = types.KeyboardButton('Баланс')
        itembtn4 = types.KeyboardButton('Купить продукт')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.send_message(message.chat.id, "У вас недостоточно балансa. Пожалуйста, пополните баланс", reply_markup=markup)

def negativeBalance(message, price):
    if state[message.chat.id]["balance"] <= price:
        return True
    else:
        return False


bot.polling()
