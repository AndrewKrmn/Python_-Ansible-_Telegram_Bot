import telebot
import subprocess
from telebot import types
TOKEN = "6659756402:AAGwYhea35qBozf0nED94U3UVko0BARAyy4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("Пінгануть сервак")
    item2 = types.KeyboardButton("Показати версію Ansible")
    item3 = types.KeyboardButton("Запустити скріпт Install Zabbix")
    markup.add(item1, item2, item3)
    bot.send_message(
        message.chat.id, "Вибери операцію :", reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Пінгануть сервак")
def ping_server(message):
    bash_command = "cd /etc/ansible/"
    result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    commands = "cd /etc/ansible/ && ansible linux -i hosts -m ping"
    kaka = subprocess.run(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (
        "Команда видала:\n" + kaka.stdout +
        "\nПомилка:\n" + kaka.stderr +
        "\nВихідний код: " + str(kaka.returncode)
    )
    bot.send_message(message.chat.id, response_message)
@bot.message_handler(func=lambda message: message.text == "Показати версію Ansible")
def version_ansible(message):
    bash_command = "ansible --version"
    result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (
        "Команда видала:\n" + result.stdout +
        "\nПомилка:\n" + result.stderr +
        "\nВихідний код: " + str(result.returncode)
    )
    bot.send_message(message.chat.id, response_message)
@bot.message_handler(func=lambda message: message.text == "Запустити скріпт Install Zabbix")
def install_zabbix(message):
    bot.reply_to(message, "Starting Zabbix installation...")
    command = "cd /home/kaka/ && bash Zabbix.sh"
    try:
        subprocess.run(command, check=True,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        bot.reply_to(message, "Zabbix installation completed successfully!")
    except subprocess.CalledProcessError:
        bot.reply_to(message, "An error occurred during the installation process.")
bot.infinity_polling()
