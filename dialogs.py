from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    start_new_user: str = "Привет! Скоро экзамены. Порешаем задания?"
    btn_var: str = f"Хочу решить целый вариант"
    btn_one: str = f"Хочу решать по одному заданию"
    exam_row: str = "{i}. {name}"
    before_check: str = "Я прислал тебе вариант.\n Нажми 'Получить ответы' и проверь себя"
    check: str = "Получить ответы"
    before_test: str = "Теперь перейди в настройки и выбери в меню удобный формат занятия"
    if_by_var: str = "Отлично! Готовлю вариант! Это может занять какое-то время."
    if_by_one: str = "Будем решать по одному!"
    next_ex: str = "Следующее задание"
    set_exams: str = "Выбери экзамен. \n{exams}"
    solution: str = "Ответ"
    too_long: str = " Я формирую вопросы. Мне потребуется время.."
    results: str = "Твои результаты за сегодня:"
    no_results: str = "Заданий больше нет"
    final_total: str = "Всего:"
    final_correct: str = "Решено верно:"
    correct_answer: str = "Верно!"
    wrong_answer: str = "Неверно! Можешь посмотреть ответ и перейти к следующему заданию"
msg = Messages()
