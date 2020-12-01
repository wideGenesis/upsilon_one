import os
import time
import dialogflow_v2 as dialogflow
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
import configparser

config = configparser.ConfigParser()
config.read("/home/genesis/projects/nauvoo_config/config.ini")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/genesis/projects/nauvoo_config/Common Bot 1-43c490d227df.json"


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


class MyLogsHandler(logging.Handler):
    def emit(self, record):
        logger_bot = config['Telegram']['bridge']
        owner = config['Telegram']['god']
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=logger_bot)
        bot_error.send_message(chat_id=owner, text=log_entry)


def echo(bot, update):
    chat_id = bot.message.chat_id
    print(chat_id, '@@@@@@@@@@@@@@@@@')
    user_message = bot.message.text
    project_id = 'common-bot-1'
    try:
        bot_answer = detect_intent_texts(project_id, chat_id, user_message, 'ru-RU')
        bot.message.reply_text(bot_answer)
    except Exception:
        logger.exception("Проблема при получении и отправке сообщений")

# Фразы
# Сбор данных


def start_command(bot, update):
    bot.message.reply_text('Ignition')


if __name__ == '__main__': 
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Запуск бота завершен!")
    
    try:
        telegram_token = '1258419809:AAG-Fq0zqF8P6DfwJL8PNz3LUDUqUx3cbqA'
        updater = Updater(telegram_token, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start",  start_command))

        echo_handler = MessageHandler(Filters.text, echo)
        dispatcher.add_handler(echo_handler)

        updater.start_polling()
        updater.idle()
        
    except Exception:
        logger.exception('Возникла ошибка в боте для общения в Телеграме ↓')

