import os
import dialogflow_v2 as dialogflow
import telegram
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
        telegram_token_information_message = config['Telegram']['bridge']
        chat_id_information_message = config['Telegram']['god']
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=telegram_token_information_message)
        bot_error.send_message(chat_id=chat_id_information_message, text=log_entry)
