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

AGE, CHECK_AGE, MAIN_MENU, MARATHON, QA, PAIN, INFO, ROUTE, SELECT_CAT, HEALTH_Q, ANSWER, SELECT_DISEASE, \
    LEG_FA, LEG_Q1, LEG_Q2, LEG_Q3, LEG_Q4, LEG_Q5, LEG_Q6 = range(19)

chat = dict()
typing = telegram.ChatAction.TYPING


def kbd(k):
    return telegram.ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True)


def flatten(nl):
    return [item for sublist in nl for item in sublist]


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=texts.welcome)
    return AGE


def age(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    chat[uid] = dict()
    chat[uid]['name'] = ans
    bot.sendMessage(uid, text=texts.greeting % ans, reply_markup=kbd(age_kbd))
    return CHECK_AGE


def check_age(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans not in flatten(age_kbd):
        bot.sendMessage(uid, text=texts.wrong_age % chat[uid]['name'], reply_markup=kbd(age_kbd))
        return AGE
    else:
        chat[uid]['age'] = ans
        bot.sendMessage(uid, text=texts.main_menu % chat[uid]['name'], reply_markup=kbd(main_kbd))
        return MAIN_MENU


def main_menu(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if main_menu_kbd[0][0] in ans:
        bot.sendMessage(uid, text=texts.main_menu % chat[uid]['name'], reply_markup=kbd(main_kbd))
        return MAIN_MENU
    else:
        bot.sendMessage(uid,
        text="Ага %s, вопрос спрашиваешь!! постараюсь ответить, но в другой раз ахахах" % chat[uid]['name'], reply_markup=kbd(main_kbd))
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


def diseases(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_disease, reply_markup=kbd(diseases_kbd))
    return SELECT_DISEASE


def leg_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[1 - 1], reply_markup=kbd(yes_no_kbd))
    return LEG_Q2


def leg_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[2 - 1], reply_markup=kbd(yes_no_kbd))
    return LEG_Q3


def leg_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[3 - 1], reply_markup=kbd(yes_no_kbd))
    return LEG_Q4


def leg_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[4 - 1], reply_markup=kbd(yes_no_kbd))
    return LEG_Q5


def leg_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[5 - 1], reply_markup=kbd(yes_no_kbd))
    return LEG_Q6


def leg_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[6-1], reply_markup=kbd(yes_no_kbd))
    return LEG_FA


def leg_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[1 - 1], reply_markup=kbd(main_kbd))
    return MAIN_MENU


def leg_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[2 - 1], reply_markup=kbd(main_kbd))
    return MAIN_MENU


def leg_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[3 - 1], reply_markup=kbd(main_kbd))
    return MAIN_MENU


def leg_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[4 - 1], reply_markup=kbd(main_kbd))
    return MAIN_MENU


def leg_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[5 - 1], reply_markup=kbd(main_kbd))
    return MAIN_MENU


def leg_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.leg_a6y, reply_markup=kbd(main_kbd))
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.leg_a6n, reply_markup=kbd(main_kbd))
    return MAIN_MENU


def back_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text="zaglushka", reply_markup=kbd(main_kbd))
    return MAIN_MENU


def answer_disease(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text="zaglushka-otvet", reply_markup=kbd(main_kbd))
    return MAIN_MENU


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
            AGE: [MessageHandler([Filters.text], age)],
            CHECK_AGE: [MessageHandler([Filters.text], check_age)],
            MAIN_MENU: [RegexHandler(main_kbd[0][0], about),
                        RegexHandler(main_kbd[0][1], qa),
                        RegexHandler(main_kbd[1][0], diseases),
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
            SELECT_DISEASE: [RegexHandler(flatten(diseases_kbd)[0], leg_q1),
                             RegexHandler(flatten(diseases_kbd)[1], back_q1),
                             RegexHandler(flatten(diseases_kbd)[2], back_q1),
                             RegexHandler(flatten(diseases_kbd)[3], back_q1),
                             RegexHandler(flatten(diseases_kbd)[4], back_q1),
                             RegexHandler(flatten(diseases_kbd)[5], back_q1),
                             RegexHandler(flatten(diseases_kbd)[6], back_q1),
                             RegexHandler(flatten(diseases_kbd)[7], main_menu),
                             MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a1),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q3),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q3: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a2),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q4),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q4: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a3),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q5),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q5: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a4),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q6),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a5),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q6),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_FA: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a6),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_a6),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
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
