async_bot для подсчета длины youtube_плейлиста
========================
About
-------------------------
**Плейлист, Видео, Канал** далее **П, В, К** соответственно.

Основной функцией бота служит получение общей длительности **П** из YouTube.
Бот ожидает получить URL-ссылку на **П** или на любой другой из предложенных объектов. 
Ответом служит краткое info о присланном объекте, c возможностью дальшейнего просмотра info всех **П** с запрошенного **К**.
***
Setup:
-------------------------
Windows:
>Редактировать bot_run.bat
    
    nano bot_run.bat images/edit bot_run.bat.jpg
    
![Alt-текст](https://github.com/pbkrd/async_bot_youtube/blob/b6bf3f86a87eb2dafdacebb3f930a8456b9e2c53/images/edit%20bot_run.bat.jpg "edit_bot_run.bat")

>Создать тестовое окружение:

    python -m venv venv
>Активировать его:

    source venv/bin/activate
>Установить зависимости:

    pip install -r requirements.txt
>Запустить скрипт:

    start bot_run.bat
___
Features
-------------------------
* Устройство клиента YouTube теперь не имеет значения.
