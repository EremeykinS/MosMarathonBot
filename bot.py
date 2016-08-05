from config import *
from keyboards import *
import texts
# from wit import Wit
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Maraphon_test_bot.' + __name__)

NAME, AGE, MAIN_MENU, MARATHON, QA, PAIN, ABOUT = range(7)

chat = dict()
typing = telegram.ChatAction.TYPING


def kbd(k):
    return telegram.ReplyKeyboardMarkup(k, one_time_keyboard=True)


def flatten(nl):
    return [item for sublist in nl for item in sublist]


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=texts.welcome)
    return NAME


def name(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    chat[uid] = dict()
    chat[uid]['name'] = ans
    chat[uid]['prev_state'] = NAME
    bot.sendMessage(uid, text=texts.greeting % ans, reply_markup=kbd(age_kbd))
    return MAIN_MENU


def main_menu(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if chat[uid]['prev_state'] == NAME:
        chat[uid]['prev_state'] = MAIN_MENU
        chat[uid]['age'] = ans
        bot.sendMessage(uid, text=texts.main_menu % chat[uid]['name'], reply_markup=kbd(main_kbd))
        return MAIN_MENU
    elif chat[uid]['prev_state'] == MAIN_MENU:
        chat[uid]['prev_state'] = MAIN_MENU
        if ans not in flatten(main_kbd):
            bot.sendMessage(uid, text="Ага %s, вопрос спрашиваешь!! постараюсь ответить, но в другой раз ахахах" % chat[uid]['name'], reply_markup=kbd(main_kbd))
            return MAIN_MENU


def about(bot, update):
    uid = update.message.from_user.id
    bot.sendMessage(uid, text=main_kbd[1][1] + "?? О как... ну ладно, " + main_kbd[1][1] + ", %s!" % chat[uid]['name'], reply_markup=kbd(main_kbd))


def qa(bot, update):
    uid = update.message.from_user.id
    bot.sendMessage(uid, text="Тут будет множество кнопок со всякой фигней!", reply_markup=kbd(main_kbd))


def pain(bot, update):
    uid = update.message.from_user.id
    bot.sendMessage(uid, text="Тут будет все про БОЛЬ !", reply_markup=kbd(main_kbd))


def marathon(bot, update):
    uid = update.message.from_user.id
    bot.sendMessage(uid, text="Тут будут красивые картинки!", reply_markup=kbd(main_kbd))


def helper(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Bye! I hope we can talk again some day.')
    return ConversationHandler.END


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [MessageHandler([Filters.text], name)],
            MAIN_MENU: [RegexHandler(main_kbd[0][0], marathon),
                        RegexHandler(main_kbd[0][1], qa),
                        RegexHandler(main_kbd[1][0], pain),
                        RegexHandler(main_kbd[1][1], about),
                        MessageHandler([Filters.text], main_menu)],
            ABOUT: [MessageHandler([Filters.text], about)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
