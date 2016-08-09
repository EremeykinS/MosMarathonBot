from config import *
from keyboards import *
import texts
import img
from wit import Wit
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import telegram
import pickle

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Marathon_test_bot.' + __name__)

AGE, CHECK_AGE, MAIN_MENU, MARATHON, QA, PAIN, INFO, ROUTE, SELECT_CAT, HEALTH_Q, ANSWER, SELECT_DISEASE, \
    LEG_FA, LEG_Q1, LEG_Q2, LEG_Q3, LEG_Q4, LEG_Q5, LEG_Q6, BACK_FA, BACK_Q2, BACK_Q3, BACK_Q4, BACK_Q5, \
    BACK_Q6, BACK_Q7, CHEST_FA, CHEST_Q2, CHEST_Q3, CHEST_Q4, CHEST_Q5, CHEST_Q6, CHEST_Q7, CHEST_Q8, \
    HAND_FA, HAND_Q2, HAND_Q3, HAND_Q4, HAND_Q5, HAND_Q6, HAND_Q7, HAND_Q8, HAND_Q9, HAND_Q10, \
    APNEA_FA, APNEA_Q1, APNEA_Q2, APNEA_Q3, APNEA_Q4, APNEA_Q5, APNEA_Q6, \
    CONVULSION_FA, CONVULSION_Q2, CONVULSION_Q3, CONVULSION_Q4, CONVULSION_Q5, CONVULSION_Q6, CONVULSION_Q7, \
    CONVULSION_Q8, HEALTH_ALL, HEALTH_CHECK = range(61)

typing = telegram.ChatAction.TYPING
chat = dict()
client = Wit(access_token=wit_token, actions=dict())


def kbd(k):
    return telegram.ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True)


def flatten(nl):
    return [item for sublist in nl for item in sublist]


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text=texts.welcome, parse_mode="HTML")
    return AGE


def age(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if chat.get(uid) is None:
        chat[uid] = dict()
        chat[uid]['name'] = ans
        bot.sendMessage(uid, text=texts.greeting % ans, reply_markup=kbd(age_kbd), parse_mode="HTML")
    else:
        bot.sendMessage(uid, text=texts.greeting % chat[uid]['name'], reply_markup=kbd(age_kbd), parse_mode="HTML")
    return CHECK_AGE


def check_age(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans not in flatten(age_kbd):
        bot.sendMessage(uid, text=texts.wrong_age % chat[uid]['name'], reply_markup=kbd(age_kbd), parse_mode="HTML")
        return CHECK_AGE
    else:
        chat[uid]['age'] = ans
        bot.sendMessage(uid, text=texts.check_health, reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
        return HEALTH_CHECK


def no_health_check(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.no_check_health % chat[uid]['name'], reply_markup=kbd(main_kbd), parse_mode="HTML")
    return MAIN_MENU


def main_menu(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if main_menu_kbd[0][0] in ans:
        bot.sendMessage(uid, text=texts.main_menu % chat[uid]['name'], reply_markup=kbd(main_kbd), parse_mode="HTML")
    else:
        client_answer = client.message(ans)
        try:
            if client_answer['entities']['intent'][0]['confidence'] < 0.6:
                bot.sendMessage(uid, text=texts.unknown_q, reply_markup=kbd(main_kbd), parse_mode="HTML")
            else:
                codec = client_answer['entities']['intent'][0]['value']
                text = texts.dictionary[codec]
                bot.sendMessage(uid, text=text, reply_markup=kbd(main_kbd))
        except KeyError:
            bot.sendMessage(uid, text=texts.unknown_q, reply_markup=kbd(main_kbd), parse_mode="HTML")
    return MAIN_MENU


def info(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.info, reply_markup=kbd(main_kbd), parse_mode="HTML")
    return MAIN_MENU


def qa(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_cat, reply_markup=kbd(main_cat_kbd), parse_mode="HTML")
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
    bot.sendMessage(uid, text=texts.select_q, reply_markup=kbd([[texts.first_time_q], [texts.back_to_all_cat_btn]]),
                    parse_mode="HTML")
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
    next_state = ANSWER
    if ans == flatten(health_cat_kbd)[0]:
        keyboard = health_c1_q_kbd
    elif ans == flatten(health_cat_kbd)[1]:
        keyboard = health_c2_q_kbd
    elif ans == flatten(health_cat_kbd)[2]:
        next_state = SELECT_CAT
        keyboard = main_cat_kbd
    bot.sendMessage(uid, text=texts.select_q, reply_markup=kbd(keyboard), parse_mode="HTML")
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


def health_all(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.health_all, reply_markup=kbd(health_all_kbd), parse_mode="HTML")
    return HEALTH_ALL


def diseases(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.select_disease, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def show_diseases(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.diseases, reply_markup=kbd(health_all_kbd), parse_mode="HTML")
    return HEALTH_ALL


def leg_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[1 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return LEG_Q2


def leg_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[2 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return LEG_Q3


def leg_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[3 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return LEG_Q4


def leg_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[4 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return LEG_Q5


def leg_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[5 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return LEG_Q6


def leg_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_q[6 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return LEG_FA


def leg_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[1 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def leg_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[2 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def leg_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[3 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def leg_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[4 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def leg_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.leg_a[5 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def leg_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.leg_a6y, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.leg_a6n, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[1 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_Q2


def back_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[2 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_Q3


def back_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[3 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_Q4


def back_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[4 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_Q5


def back_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[5 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_Q6


def back_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[6 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_Q7


def back_q7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_q[7 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return BACK_FA


def back_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_a[1 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_a[2 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_a[3 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_a[4 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_a[5 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.back_a[6 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def back_a7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.back_a7y, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.back_a7n, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[1 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q2


def chest_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[2 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q3


def chest_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[3 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q4


def chest_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[4 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q5


def chest_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[5 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q6


def chest_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[6 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q7


def chest_q7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[7 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_Q8


def chest_q8(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_q[8 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CHEST_FA


def chest_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[1 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[2 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[3 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[4 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[5 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[6 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.chest_a[7 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def chest_a8(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.chest_a8y, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.chest_a8n, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[1 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q2


def hand_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[2 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q3


def hand_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[3 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q4


def hand_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[4 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q5


def hand_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[5 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q6


def hand_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[6 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q7


def hand_q7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[7 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q8


def hand_q8(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[8 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q9


def hand_q9(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[9 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_Q10


def hand_q10(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_q[10 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return HAND_FA


def hand_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[1 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[2 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[3 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[4 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[5 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[6 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[7 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a8(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[8 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a9(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.hand_a[9 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def hand_a10(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.hand_a10y, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.hand_a10n, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def apnea_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_q[1 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return APNEA_Q2


def apnea_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_q[2 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return APNEA_Q3


def apnea_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_q[3 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return APNEA_Q4


def apnea_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_q[4 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return APNEA_Q5


def apnea_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_q[5 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return APNEA_Q6


def apnea_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_q[6 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return APNEA_FA


def apnea_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_a[1 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def apnea_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_a[2 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def apnea_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_a[3 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def apnea_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_a[4 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def apnea_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.apnea_a[5 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def apnea_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.apnea_a6y, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.apnea_a6n, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[1 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q2


def convulsion_q2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[2 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q3


def convulsion_q3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[3 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q4


def convulsion_q4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[4 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q5


def convulsion_q5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[5 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q6


def convulsion_q6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[6 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q7


def convulsion_q7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[7 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_Q8


def convulsion_q8(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_q[8 - 1], reply_markup=kbd(yes_no_kbd), parse_mode="HTML")
    return CONVULSION_FA


def convulsion_a1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[1 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a2(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[2 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a3(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[3 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a4(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[4 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a5(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[5 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a6(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[6 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a7(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.convulsion_a[7 - 1], reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def convulsion_a8(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    ans = update.message.text
    if ans == flatten(yes_no_kbd)[yes]:
        bot.sendMessage(uid, text=texts.convulsion_a8y, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    elif ans == flatten(yes_no_kbd)[no]:
        bot.sendMessage(uid, text=texts.convulsion_a8n, reply_markup=kbd(diseases_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def nothing_q1(bot, update):
    uid = update.message.from_user.id
    bot.sendChatAction(uid, action=typing)
    bot.sendMessage(uid, text=texts.no_disease, reply_markup=kbd(main_menu_kbd), parse_mode="HTML")
    return SELECT_DISEASE


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    global chat
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

            HEALTH_CHECK: [RegexHandler(flatten(yes_no_kbd)[yes], diseases),
                           RegexHandler(flatten(yes_no_kbd)[no], no_health_check)],

            MAIN_MENU: [RegexHandler(flatten(main_kbd)[0], about),
                        RegexHandler(flatten(main_kbd)[1], qa),
                        RegexHandler(flatten(main_kbd)[2], health_all),
                        RegexHandler(flatten(main_kbd)[3], info),
                        MessageHandler([Filters.text], main_menu)] + command_handlers,

            INFO: [MessageHandler([Filters.text], info)] + command_handlers,

            MARATHON: [RegexHandler(flatten(marathon_kbd)[0], schedule),
                       RegexHandler(flatten(marathon_kbd)[1], route),
                       RegexHandler(flatten(marathon_kbd)[2], main_menu),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,

            ROUTE: [RegexHandler(flatten(distance_kbd)[0], distance_42),
                    RegexHandler(flatten(distance_kbd)[1], distance_10),
                    RegexHandler(flatten(distance_kbd)[2], main_menu),
                    MessageHandler([Filters.text], main_menu)] + command_handlers,

            SELECT_CAT: [RegexHandler(flatten(main_cat_kbd)[0], start_q),
                         RegexHandler(flatten(main_cat_kbd)[1], health_cats),
                         RegexHandler(flatten(main_cat_kbd)[2], clothes_q),
                         RegexHandler(flatten(main_cat_kbd)[3], regime_q),
                         RegexHandler(flatten(main_cat_kbd)[4], main_menu),
                         MessageHandler([Filters.text], main_menu)] + command_handlers,

            HEALTH_Q: [MessageHandler([Filters.text], health_q)] + command_handlers,

            ANSWER: [MessageHandler([Filters.text], answer)] + command_handlers,

            HEALTH_ALL: [RegexHandler(flatten(health_all_kbd)[0], diseases),
                         RegexHandler(flatten(health_all_kbd)[1], show_diseases),
                         RegexHandler(flatten(health_all_kbd)[2], main_menu)] + command_handlers,

            SELECT_DISEASE: [RegexHandler(flatten(diseases_kbd)[0], leg_q1),
                             RegexHandler(flatten(diseases_kbd)[1], back_q1),
                             RegexHandler(flatten(diseases_kbd)[2], chest_q1),
                             RegexHandler(flatten(diseases_kbd)[3], hand_q1),
                             RegexHandler(flatten(diseases_kbd)[4], apnea_q1),
                             RegexHandler(flatten(diseases_kbd)[5], convulsion_q1),
                             RegexHandler(flatten(diseases_kbd)[6], nothing_q1),
                             RegexHandler(flatten(diseases_kbd)[7], main_menu),
                             MessageHandler([Filters.text], main_menu)] + command_handlers,

            LEG_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a1),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q2),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q3: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a2),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q3),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q4: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a3),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q4),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q5: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a4),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q5),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a5),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_q6),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,
            LEG_FA: [RegexHandler(flatten(yes_no_kbd)[yes], leg_a6),
                     RegexHandler(flatten(yes_no_kbd)[no], leg_a6),
                     MessageHandler([Filters.text], main_menu)] + command_handlers,

            BACK_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], back_a1),
                      RegexHandler(flatten(yes_no_kbd)[no], back_q2),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            BACK_Q3: [RegexHandler(flatten(yes_no_kbd)[yes], back_a2),
                      RegexHandler(flatten(yes_no_kbd)[no], back_q3),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            BACK_Q4: [RegexHandler(flatten(yes_no_kbd)[yes], back_a3),
                      RegexHandler(flatten(yes_no_kbd)[no], back_q4),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            BACK_Q5: [RegexHandler(flatten(yes_no_kbd)[no], back_a4),
                      RegexHandler(flatten(yes_no_kbd)[yes], back_q5),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            BACK_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], back_a5),
                      RegexHandler(flatten(yes_no_kbd)[no], back_q6),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            BACK_Q7: [RegexHandler(flatten(yes_no_kbd)[yes], back_a6),
                      RegexHandler(flatten(yes_no_kbd)[no], back_q7),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            BACK_FA: [RegexHandler(flatten(yes_no_kbd)[yes], back_a7),
                      RegexHandler(flatten(yes_no_kbd)[no], back_a7),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,

            CHEST_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], chest_a1),
                       RegexHandler(flatten(yes_no_kbd)[no], chest_q2),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_Q3: [RegexHandler(flatten(yes_no_kbd)[no], chest_a2),
                       RegexHandler(flatten(yes_no_kbd)[yes], chest_q3),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_Q4: [RegexHandler(flatten(yes_no_kbd)[no], chest_a3),
                       RegexHandler(flatten(yes_no_kbd)[yes], chest_q4),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_Q5: [RegexHandler(flatten(yes_no_kbd)[yes], chest_a4),
                       RegexHandler(flatten(yes_no_kbd)[no], chest_q5),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], chest_a5),
                       RegexHandler(flatten(yes_no_kbd)[no], chest_q6),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_Q7: [RegexHandler(flatten(yes_no_kbd)[yes], chest_a6),
                       RegexHandler(flatten(yes_no_kbd)[no], chest_q7),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_Q8: [RegexHandler(flatten(yes_no_kbd)[yes], chest_a7),
                       RegexHandler(flatten(yes_no_kbd)[no], chest_q8),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            CHEST_FA: [RegexHandler(flatten(yes_no_kbd)[yes], chest_a8),
                       RegexHandler(flatten(yes_no_kbd)[no], chest_a8),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,

            HAND_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a1),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q2),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q3: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a2),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q3),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q4: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a3),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q4),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q5: [RegexHandler(flatten(yes_no_kbd)[no], hand_a4),
                      RegexHandler(flatten(yes_no_kbd)[yes], hand_q5),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a5),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q6),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q7: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a6),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q7),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q8: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a7),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q8),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q9: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a8),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_q9),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_Q10: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a9),
                       RegexHandler(flatten(yes_no_kbd)[no], hand_q10),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            HAND_FA: [RegexHandler(flatten(yes_no_kbd)[yes], hand_a10),
                      RegexHandler(flatten(yes_no_kbd)[no], hand_a10),
                      MessageHandler([Filters.text], main_menu)] + command_handlers,

            APNEA_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], apnea_a1),
                       RegexHandler(flatten(yes_no_kbd)[no], apnea_q2),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            APNEA_Q3: [RegexHandler(flatten(yes_no_kbd)[yes], apnea_a2),
                       RegexHandler(flatten(yes_no_kbd)[no], apnea_q3),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            APNEA_Q4: [RegexHandler(flatten(yes_no_kbd)[yes], apnea_a3),
                       RegexHandler(flatten(yes_no_kbd)[no], apnea_q4),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            APNEA_Q5: [RegexHandler(flatten(yes_no_kbd)[yes], apnea_a4),
                       RegexHandler(flatten(yes_no_kbd)[no], apnea_q5),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            APNEA_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], apnea_a5),
                       RegexHandler(flatten(yes_no_kbd)[no], apnea_q6),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,
            APNEA_FA: [RegexHandler(flatten(yes_no_kbd)[yes], apnea_a6),
                       RegexHandler(flatten(yes_no_kbd)[no], apnea_a6),
                       MessageHandler([Filters.text], main_menu)] + command_handlers,

            CONVULSION_Q2: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a1),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q2),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_Q3: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a2),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q3),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_Q4: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a3),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q4),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_Q5: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a4),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q5),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_Q6: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a5),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q6),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_Q7: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a6),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q7),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_Q8: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a7),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_q8),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
            CONVULSION_FA: [RegexHandler(flatten(yes_no_kbd)[yes], convulsion_a8),
                            RegexHandler(flatten(yes_no_kbd)[no], convulsion_a8),
                            MessageHandler([Filters.text], main_menu)] + command_handlers,
        },

        fallbacks=[]
    )

    data_saved = True
    conversations_file = 'conversations'
    try:
        open(conversations_file, mode='rb')
    except IOError as e:
        print('не удалось открыть файл')
        data_saved = False

    if data_saved:
        chat, conv_handler.conversations = pickle.load(open(conversations_file, mode='rb'))

    dp.add_handler(conv_handler)

    # updater.start_polling()
    #
    # updater.idle()



    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    pickle.dump((chat, conv_handler.conversations), open(conversations_file, mode='wb'))
    print('saved')


if __name__ == '__main__':
    main()
