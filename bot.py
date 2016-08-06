from config import *
from keyboards import *
import texts
import img
# from wit import Wit
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Marathon_test_bot.' + __name__)

NAME, AGE, MAIN_MENU, MARATHON, QA, PAIN, INFO, ROUTE, SELECT_CAT, HEALTH_Q, ANSWER = range(11)

chat = dict()
typing = telegram.ChatAction.TYPING


def kbd(k):
    return telegram.ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True)


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
    elif ans == main_menu_kbd[0][0]:
        bot.sendMessage(uid, text="Ну все %s, ты в главном меню ахахах" % chat[uid]['name'], reply_markup=kbd(main_kbd))
        return MAIN_MENU
    elif chat[uid]['prev_state'] == MAIN_MENU:
        chat[uid]['prev_state'] = MAIN_MENU
        if ans not in flatten(main_kbd):
            bot.sendMessage(uid,
                            text="Ага %s, вопрос спрашиваешь!! постараюсь ответить, но в другой раз ахахах" % chat[uid][
                                'name'], reply_markup=kbd(main_kbd))
            return MAIN_MENU


def info(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.info, reply_markup=kbd(main_kbd), parse_mode="HTML")
    return MAIN_MENU


def qa(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_cat, reply_markup=kbd(main_cat_kbd))
    return SELECT_CAT


def pain(bot, update):
    uid = update.message.from_user.id
    bot.sendMessage(uid, text="Тут будет все про БОЛЬ !", reply_markup=kbd(main_kbd))


def about(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.about_marathon, reply_markup=kbd(marathon_kbd), parse_mode="HTML")
    return MARATHON


def route(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.route, reply_markup=kbd(distance_kbd), parse_mode="HTML")
    return ROUTE


def schedule(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.schedule, reply_markup=kbd(marathon_kbd), parse_mode="HTML")


def distance_42(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.route_42km, parse_mode="HTML")
    bot.sendPhoto(uid, photo=img.route_42km, reply_markup=kbd(distance_kbd))


def distance_10(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.route_10km, parse_mode="HTML")
    bot.sendPhoto(uid, photo=img.route_10km, reply_markup=kbd(distance_kbd))


def start_q(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_q, reply_markup=kbd([[texts.first_time_q], [texts.back_to_all_cat_btn]]))
    return ANSWER


def health_cats(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_sub_cat, reply_markup=kbd(health_cat_kbd), parse_mode="HTML")
    return HEALTH_Q


def health_q(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    # text = texts.select_q
    next_state = ANSWER
    if ans == flatten(health_cat_kbd)[0]:
        keyboard = health_c1_q_kbd
    elif ans == flatten(health_cat_kbd)[1]:
        keyboard = health_c2_q_kbd
    elif ans == flatten(health_cat_kbd)[2]:
        next_state = SELECT_CAT
        # text = texts.select_cat
        keyboard = main_cat_kbd
    bot.sendMessage(uid, text=texts.select_q, reply_markup=kbd(keyboard))
    return next_state


def clothes_q(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_q, reply_markup=kbd(clothes_q_kbd), parse_mode="HTML")
    return ANSWER


def regime_q(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_q, reply_markup=kbd(regime_q_kbd), parse_mode="HTML")
    return ANSWER


def answer(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    next_state = ANSWER
    if ans == texts.first_time_q:
        print('answering...')
        text = texts.first_time_a
        keyboard = [[texts.first_time_q], [texts.back_to_all_cat_btn]]
    elif ans in texts.health_c1_q:
        text = texts.health_c1_a[texts.health_c1_q.index(ans)]
        keyboard = health_c1_q_kbd
    elif ans in texts.health_c2_q:
        text = texts.health_c2_a[texts.health_c2_q.index(ans)]
        keyboard = health_c2_q_kbd
    elif ans in texts.clothes_q:
        text = texts.clothes_a[texts.clothes_q.index(ans)]
        keyboard = clothes_q_kbd
    elif ans in texts.regime_q:
        text = texts.regime_a[texts.regime_q.index(ans)]
        keyboard = regime_q_kbd
    elif ans == texts.back_to_all_cat_btn:
        next_state = SELECT_CAT
        text = texts.select_cat
        keyboard = main_cat_kbd
    elif ans == flatten(health_c1_q_kbd)[-1]:
        next_state = HEALTH_Q
        text = texts.select_sub_cat
        keyboard = health_cat_kbd
    bot.sendMessage(uid, text=text, reply_markup=kbd(keyboard), parse_mode="HTML")
    return next_state


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

    command_handlers = [CommandHandler('start', start),
                        CommandHandler('questions', qa),
                        CommandHandler('about', about),
                        CommandHandler('info', info)]

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=command_handlers,

        states={
            NAME: [MessageHandler([Filters.text], name)],
            MAIN_MENU: [RegexHandler(main_kbd[0][0], about),
                        RegexHandler(main_kbd[0][1], qa),
                        RegexHandler(main_kbd[1][0], pain),
                        RegexHandler(main_kbd[1][1], info),
                        MessageHandler([Filters.text], main_menu)] + command_handlers,
            INFO: [MessageHandler([Filters.text], info)] + command_handlers,
            MARATHON: [RegexHandler(flatten(marathon_kbd)[0], schedule),
                       RegexHandler(flatten(marathon_kbd)[1], route),
                       RegexHandler(flatten(marathon_kbd)[2], main_menu),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            ROUTE: [RegexHandler(distance_kbd[0][0], distance_42),
                    RegexHandler(distance_kbd[0][1], distance_10),
                    RegexHandler(distance_kbd[0][2], main_menu),
                    MessageHandler([Filters.text], main_menu)] + command_handlers,
            SELECT_CAT: [RegexHandler(flatten(main_cat_kbd)[0], start_q),
                         RegexHandler(flatten(main_cat_kbd)[1], health_cats),
                         RegexHandler(flatten(main_cat_kbd)[2], clothes_q),
                         RegexHandler(flatten(main_cat_kbd)[3], regime_q),
                         RegexHandler(flatten(main_cat_kbd)[4], main_menu),
                         MessageHandler([Filters.text], main_menu)] + command_handlers,
            HEALTH_Q: [MessageHandler([Filters.text], health_q)] + command_handlers,
            ANSWER: [MessageHandler([Filters.text], answer)] + command_handlers,
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # questions_handler = CommandHandler('questions', qa)
    # about_handler = CommandHandler('about', about)
    # info_handler = CommandHandler('info', info)

    dp.add_handler(conv_handler)
    # dp.add_handler(questions_handler)
    # dp.add_handler(about_handler)
    # dp.add_handler(info_handler)

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
