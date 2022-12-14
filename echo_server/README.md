# Реализация эхо-сервера
___
## Команды
+ exit - разрывает соединения со стороны клиента.
+ stop - завершает работу сервера.




# Задания для выполнения
___
### 1. Создать простой TCP-сервер, который принимает от клиента строку (порциями по 1 КБ) и возвращает ее. (Эхо-сервер).
### 2. Сервер должен выводить в консоль служебные сообщения (с пояснениями) при наступлении любых событий:
+ Запуск сервера; 
+ Начало прослушивания порта; 
+ Подключение клиента; 
+ Прием данных от клиента; 
+ Отправка данных клиенту; 
+ Отключение клиента; 
+ Остановка сервера.
___
### Напишите простой TCP-клиент, который устанавливает соединение с сервером, считывает строку со стандартного ввода и посылает его серверу.
___
### Клиент должен выводить в консоль служебные сообщения (с пояснениями) при наступлении любых событий:
+ Соединение с сервером; 
+ Разрыв соединения с сервером; 
+ Отправка данных серверу; 
+ Прием данных от сервера.
___
### Контрольные вопросы
+ Чем отличаются клиентские и серверные сокеты?
  + серверные сокеты - это сокет, имеющий определенный IP-адрес, предполагающий обмен данными с клиентом. Может работать с несколькими клиентами одновременно.
  + клиентские сокеты - может запускаться на любом устройстве и должен знать IP-адрес сервера, отправляет запрос на сервер. 
+ Как можно передавать через сокеты текстовую информацию?
  + После запроса текстовой информации, она преобразовывается в байтовый вид encode() и отправляется на сервер с помощью метода send()/
+ Какие операции с сокетами блокируют выполнение программы?
  + accept(), connect() и recv(). Это значит, что после их вызова выполнение программы остановится и не возобновится до тех пор, пока не поступят соответствующие данные из сети. А если программа не выполняется, то и другие соединения и задачи также не обрабатываются.
+ Что такое неблокирующие сокеты?
  + функция чтения проверяет, есть ли данные в буфере, и если есть - сразу возвращает, если нет, то она не ждет и также сразу возвращает, что прочитано 0 байт.
+ В чем преимущества и недостатки использования TCP по сравнению с UDP?
  + UDP - потоковый, быстрый протокол передачи данных без гарантии целостности данных.
  + TCP - диалоговый, более медленный, гарантирует целостность данных.
+ Какие системные вызовы, связанные с сокетами используются только на стороне сервера?
  + 
+ На каком уровне модели OSI работают сокеты?
  + Транспортный уровень.
+ Почему однопоточное приложение не может решить задачу одновременного подключения? 
  + 
+ Чем поток отличается от процесса? 
  + 
+ Как создать новый поток? 
  + Создание нового потока с помощью Thread() и запуск вызываемого объекта в отдельном потоке Thread().start()
+ Как выделить участок кода так, чтобы он выполнялся в другом потоке?
  + 
+ В чем проблема потокобезопасности?
  + 
+ Какие методы обеспечения потокобезопасности существуют?
  + threading 
  + lock - это примитив синхронизации: механизм, обеспечивающий ограничения доступа к ресурсу при наличии множества потоков выполнения.
___
### Задания для самостоятельного выполнения
+ Проверьте возможность подключения к серверу с локальной, виртуальной и удаленной машины.
+ Модифицируйте код сервера таким образом, чтобы он читал строки в цикле до тех пор, пока клиент не введет “exit”. Можно считать, что это команда разрыва соединения со стороны клиента.
+ Модифицируйте код сервера таким образом, чтобы при разрыве соединения клиентом он продолжал слушать данный порт и, таким образом, был доступен для повторного подключения.
+ Модифицируйте код клиента и сервера таким образом, чтобы номер порта и имя хоста (для клиента) они спрашивали у пользователя. Реализовать безопасный ввод данных и значения по умолчанию.
+ Модифицировать код сервера таким образом, чтобы все служебные сообщения выводились не в консоль, а в специальный лог-файл.
+ Модифицируйте код сервера таким образом, чтобы он автоматически изменял номер порта, если он уже занят. Сервер должен выводить в консоль номер порта, который он слушает.
+ Реализовать сервер идентификации. Сервер должен принимать соединения от клиента и проверять, известен ли ему уже этот клиент (по IP-адресу). Если известен, то поприветствовать его по имени. Если неизвестен, то запросить у пользователя имя и записать его в файл. Файл хранить в произвольном формате.
+ Реализовать сервер аутентификации. Похоже на предыдущее задание, но вместе с именем пользователя сервер отслеживает и проверяет пароли. Дополнительные баллы за безопасное хранение паролей. Дополнительные баллы за поддержание сессии на основе токена наподобие cookies
+ Напишите вспомогательные функции, которые реализуют отправку и принятие текстовых сообщений в сокет. Функция отправки должна дополнять сообщение заголовком фиксированной длины, в котором содержится информация о длине сообщения. Функция принятия должна читать сообщение с учетом заголовка. В дополнении реализуйте преобразование строки в байтовый массив и обратно в этих же функциях. Дополнително оценивается, если эти функции будут реализованы как унаследованное расширение класса socket библиотеки socket.
+ Дополните код клиента и сервера таким образом, чтобы они могли посылать друг другу множественные сообщения один в ответ на другое.
+ Напишите многопользовательский чат. Подсказка: используйте сокеты, основанные на протоколе UDP.
+ Реализовать сканер TCP-портов. Программа должна запрашивать имя хоста/IP-адрес у пользователя. Затем программа должна пробовать подключиться к этому хосту ко всем портами по очереди. При успешном подключении программа должна выводить в консоль сообщение “Порт N открыт”. 
  + Модифицировать эту программу, чтобы сканирование портов происходило параллельно. Для этого нужно распараллелить сканирование портов по нескольким потокам.
  + Обеспечить вывод списка открытых портов по порядку. 
  + Реализовать progress bar в командной строке, показывающий прогресс сканирования.
+ Модифицировать простой эхо-сервер таким образом, чтобы при подключении клиента создавался новый поток, в котором происходило взаимодействие с ним. 
+ Реализовать простой чат сервер на базе сервера аутентификации. Сервер должен обеспечивать подключение многих пользователей одновременно, отслеживание имен пользователей, поддерживать историю сообщений и пересылку сообщений от каждого пользователя всем остальным. 
+ Реализовать сервер с управляющим потоком. При создании сервера прослушивание портов происходит в отдельном потоке, а главный поток программы в это время способен принимать команды от пользователя. Необходимо реализовать следующие команды:
  + Отключение сервера (завершение программы); 
  + Пауза (остановка прослушивание порта); 
  + Показ логов; 
  + Очистка логов; 
  + Очистка файла идентификации.