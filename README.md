# telegram_bot_sdamgia
## Бот, позволяющий решать задания ЕГЭ по выбранному предмету в режиме реального времени
[SdamGiaBot](http://t.me/Sdamgia_test_bot)

Использованные API: https://ege.sdamgia.ru/, sdamgia-api 0.1.7

### Возможности бота:
/start — выбор предмета, по которму будет сформирован вариант для решения

После выбора предмета бот обращается к сайту https://ege.sdamgia.ru, на котором формируется тестовый вариант
Так как вариант состоит из 15+ заданий, эта часть является наиболее долгой в работе бота. 

После фомирования варианта бот предлагает 2 опции, которые можно выбрать кнопками, которые расположены у клавиатуры:
  1. Загрузить и решить вариант самостоятельно, а затем запросить у бота ответы. В таком случае пользователь проверяет результаты сасмостоятельно
  2. Решать задачи по очереди. Схема взаимодействия с ботом при таком сценарии:
        1. Бот присылает задание
        2. Пользователь отправляет ответ
        3. Бот проверяет ответ и возвращает результат: верно/неверно
        4. Пользователь может посмотреть верный ответ, нажав на кнопку "Ответ"
        5. Пользователь нажимает кнопку "Следующее задание" и алгоритм повторяется
        6. Когда весь вариант решен, бот подводит статистику верно решенных заданий относительно общего количества заданий в варианте
 
 Пользователь имеет возможность в любой момент начать решать другой вариант или выбрать другой предмет с помощью кнопки /start 

Любой ввод с клавиатуры бот воспринимает как ответ на задачу
