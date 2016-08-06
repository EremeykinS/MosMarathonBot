import texts
from telegram import Emoji
back_pic = Emoji.BACK_WITH_LEFTWARDS_ARROW_ABOVE
main_menu_kbd = [["Главное меню"]]
main_kbd = [["О марафоне", "Частые вопросы"], ["Здоровье", "О Боте"]]
yes_no_kbd = [['Да', 'Нет']]
age_kbd = [["младше 18", "18-30"], ["30-45", "старше 45"]]
marathon_kbd = [["Расписание"], ["Маршрут"], ["Главное меню"]]
distance_kbd = [["42 км", "10 км", "Главное меню"]]
main_cat_kbd = [["Начало тренировок", "Здоровье"], ["Одежда и обувь", "Режим тренировок"], ["Главное меню"]]
health_cat_kbd = [["Заболевания"], ["Вес и мышцы"], [texts.back_to_all_cat_btn]]
health_c1_q_kbd = [[q] for q in texts.health_c1_q] + [[texts.back_to_health_cat_btn]]
health_c2_q_kbd = [[q] for q in texts.health_c2_q] + [[texts.back_to_health_cat_btn]]
clothes_q_kbd = [[q] for q in texts.clothes_q] + [[texts.back_to_all_cat_btn]]
regime_q_kbd = [[q] for q in texts.regime_q] + [[texts.back_to_all_cat_btn]]
