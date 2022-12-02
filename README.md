async_bot для подсчету длины youtube_плейлиста
========================
About
-------------------------
**Плейлист, Видео, Канал** далее **П, В, К** соответственно.
Основной функцией бота служит получение общей длительности **П** из YouTube.
Бот ожидает получить URL-ссылку на **П** или на любой другой из предложенных объектов. 
Ответом служит краткое info о присланном объекте, c возможностью дальшейнего просмотра info всех **П** с запрошенного **К**.
***
### Setup:
>Редактировать bot_run.bat
    
    Команда по открытию файла в редакторе
 *IMAGE*

>Создать тестовое окружение:

    python3 -m venv venv
>Активировать его:

    source venv/bin/activate
>Установить зависимости:

    pip install -r requirements.txt
>Запустить скрипт:

    bot_run.bat
___
Features
-------------------------
* Устройство клиента YouTube теперь не имеет значения.
