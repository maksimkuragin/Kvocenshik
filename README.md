# Kvocenshik
https://kvocenshik.herokuapp.com/

О проекте:
Проект предназначен для всех желающих, кто хочет сделать оценку рыночной стоимости квартиры.
На данный момент сервис работает только по квартирам в Москве.
Для того, чтобы получить предсказание необходимо ввести основные параметры квартиры: адрес, ближайшее метро, количество комнат и площадь.
Для более точного расчета можно заполнить дополнительные параметры. Нажав на кнопку "Рассчитать", происходит вся магия, и мы видим предсказание стоимости квартиры и карту с месторасположением дома, который был указан.

Пошаговое выполнение проекта:

1. Парсинг. 
Нет данных - нет Data Science, поэтому первым делом необходимо собрать данные. Обратившийсь к самому популярному агрегатору недвижимости "Циан", с помощью библиотеки Selenium и специального драйвера был написан код, который перебирал страницы с квартирами, изменяя два параметра: метро и количество комнат в квартире. Таким образом, спустя 4 часа работы кода было скачено около 4 тысяч excel файлов с данными о квартирах. 

2. Обработка и анализ данных. 
Далее начался процесс, занимающий 70% времени работы над проектом. Были удалены ненужные столбики, заполнены пропущеные значения, добавлены новые значения на основе тех, что уже есть. В ходе выполнения данных задач возникло много трудностей: 
<br>а) было необходимо написать функцию конвертирующую стоимость из валюты в рубли; 
<br>б) функцию с регулярмыми выражениями, для обработки строк с адресом, необходимую для правильного формата строковых значений для перевода адреса в координаты;
<br>в) функцию преобразования адреса в координаты с помощью библиотеки geocoder, в которой было необходимо прописать ошибки по таймингу, и в случае если адрес не найден, то заполнить значение NaN. 

Далее была проведена более точная работа над выбросами и добавление новых параметров: 
а) на основе координат было добавлено расстояние от дома до центра Москвы; 
б) на основе расстояния, окружность в которую входит квартира; 
в) на основе станций метро: район и административный округ. 

Добавление новых параметров положительно повлияло на результат предсказаний. Далее было необходимо преобразовать все категориальные фичи, заменив их на числа для более удобного формата работы на backend. Затем стандартные процедуры: нормализация, train/test split и обучение.

3. Обучение. 
Таким образом, мы подошли к самому главному - обучению. Для начала было сделано несколько модлелей без параметров 
