import asyncio
import logging
import os
import socket
import sys
from datetime import datetime

logging.basicConfig(filename='log/client.log', encoding='utf-8',
                    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s", level=logging.INFO)


class Client:
    """
    Клиент
    """

    def __init__(self, server_ip="127.0.0.1", port=2005):
        """
        Args:
            server_ip (str): localhost/ip-адресс сервера
            port (int): порт сервера
        """
        self.server_ip = server_ip
        self.port = port
        self.message = ''
        self.status = ''
        asyncio.run(self.main())

    async def main(self):
        """
        Ввод порта и ip сервера, валидация данных
        """
        user_port = input("Введите порт (enter для значения по умолчанию):") or self.port

        if not str(user_port).isdigit() or not 1024 <= int(user_port) <= 65535:
            user_port = self.port
            print(f"Установили порт {user_port} по умолчанию!")
        else:
            user_port = int(user_port)

        user_ip = input("Введите ip сервера (enter для значения по умолчанию):") or self.server_ip
        if not all(i.isdigit() or i == '.' for i in user_ip.split('.')):
            user_ip = self.server_ip
            print(f"Установили ip-адресс {user_ip} по умолчанию!")

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(user_ip, user_port), timeout=1
            )
        except (OSError, asyncio.TimeoutError):
            print(f"Не удалось присоединиться к серверу: ip-адрес: {user_ip}, порт: {user_port}")
            sys.exit(0)

        logging.info(f"Установлено соединение {writer.get_extra_info('sockname')} "
                     f"с сервером ('{user_ip}', {user_port})")

        await self.authorize(reader, writer)

    async def authorize(self, reader, writer):
        """Логика авторизации пользователя"""
        while True:
            data = await asyncio.wait_for(reader.readline(), timeout=1)
            if not data:
                sys.exit(0)
            logging.info(f"Клиент {writer.get_extra_info('sockname')} принял данные от сервера: {data}")
            data = data.decode().strip()
            if 'Здравствуйте' in data or 'Приветствую' in data:
                self.username = data.split(" ")[1]
                logging.info(f"Клиент {writer.get_extra_info('sockname')} прошел авторизацию!")
                break
            elif data == 'запрашивает пароль':
                await self.send_password(writer)
            elif data in ('запрашивает имя', "Регистрация нового пользователя"):
                await self.send_name(writer)

        task_msg_recv = asyncio.create_task(self.message_receiving(reader))

        while True:
            await asyncio.sleep(1)

    async def message_receiving(self, reader):
        """Чтение сообщения от сервера"""
        while True:
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=0.5)
                if not data:
                    await reader.aclose()
                    sys.exit(0)
                logging.info(f"Клиент {reader._transport.get_extra_info('sockname')} принял "
                             f"данные от сервера: {data}")
                data = data.decode().strip()
                if data == "show logs":
                    self.show_log()
                elif data == "clean logs":
                    await self.clean_log()
                else:
                    print(f"Сервер: {data}\n", end='')

            except (asyncio.TimeoutError, OSError):
                continue

    async def clean_log(self):
        with open('client.log', 'w', encoding='utf-8') as client_file:
            client_file.write('')
        logging.info('Очистка логов пользователя.')

    async def write_history(self, username, message):
        path = os.getcwd()
        if os.path.exists(os.path.join(path, username)):
            method = 'a+'
        else:
            method = 'w'
        with open(f'{username}.txt', method, encoding='utf-8') as client_file:
            client_file.write(f'Время:{datetime.now()} Имя:{username} Сообщение: {message}')
        logging.info('Добавили историю в файл')

    async def send_password(self, writer):
        """Отправка пароля на сервер"""
        password = input('Введите пароль:')
        writer.write(f"{password}\n".encode())
        await writer.drain()

    async def send_name(self, writer):
        """Отправка имени на сервер"""
        self.username = input(f"Введите имя:")
        writer.write(f"{self.username}\n".encode())
        await writer.drain()

    def show_log(self):
        with open('log/client.log', 'r') as f:
            lines = f.readlines()
            for line in lines:
                print(line.strip())


if __name__ == "__main__":
    client = Client()


# import socket
# import logging
# from threading import Thread
# import sys
# import pickle
# from validation import ip_validation, port_validation
# # from getpass import getpass
# from time import sleep
# import os
# import datetime
# import asyncio
#
# logging.basicConfig(filename='log/client.log', encoding='utf-8',
#                     format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s", level=logging.INFO)
#
#
# class Client:
#     """
#     Клиент
#     """
#
#     def __init__(self, server_ip, port):
#         """
#         Args:
#             server_ip (str): localhost/ip-адресс сервера
#             port (int): порт сервера
#         """
#         self.sock = None
#         self.server_ip = server_ip
#         self.port = port
#         self.message = ''
#         self.status = ''
#         asyncio.run(self.main())
#
#     async def server_connection(self):
#         """Соединение клиента с сервером"""
#         sock = socket.socket()
#         sock.setblocking(1)
#         try:
#             await asyncio.sleep(1)  # добавляем задержку для устранения блокировки ввода-вывода
#             await sock.connect((self.server_ip, self.port))
#         except ConnectionRefusedError:
#             print(f"Не удалось присоединиться к серверу: ip-адрес: {self.server_ip}, порт: {self.port}")
#             sys.exit(0)
#         self.sock = sock
#         logging.info(
#             f"Установлено соединение {self.sock.getsockname()} с сервером ('{self.server_ip}', {self.port})")
#
#     async def message_receiving(self):
#         """Ввод сообщения, проверка на exit для выхода"""
#         Thread(target=self.data_acquisition).start()
#         await asyncio.sleep(1)
#         while True:
#             # print('self.data -', self.data, type(self.data))
#             if 'Здравствуйте' in self.data or 'Приветствую' in self.data:
#                 self.welcome()
#                 break
#             elif self.data == 'запрашивает пароль':
#                 self.send_password()
#             elif self.data in ('запрашивает имя', "Регистрация нового пользователя"):
#                 self.send_name()
#         while True:
#             await asyncio.sleep(1.5)
#             self.message = input(f'\n{self.username}, ведите сообщение ("exit" для выхода):')
#             if self.message != "":
#                 if self.message.lower() == 'exit':
#                     logging.info(f"Разрыв соединения {self.sock.getsockname()} с сервером!")
#                     break
#                 time_now = datetime.datetime.now()
#                 self.write_history(time_now)
#                 send_message = pickle.dumps(['message', self.message, self.username])
#                 self.sock.sendall(send_message)
#                 logging.info(f"Отправка данных от {self.sock.getsockname()} на сервер: {self.message}")
#             elif self.message == 'show logs':
#                 self.show_log()
#             elif self.message == 'clean logs':
#                 self.clean_log()
#         self.sock.close()
#
#     async def clean_log(self):
#         with open('client.log', 'w', encoding='utf-8') as client_file:
#             client_file.write('')
#         logging.info(f'Очистка логов пользователя.')
#
#     async def write_history(self, time):
#         path = os.getcwd()
#         if os.path.exists(os.path.join(path, self.username)):
#             method = 'a+'
#         else:
#             method = 'w'
#         with open(f'{self.username}.txt', method, encoding='utf-8') as client_file:
#             client_file.write(f'Время:{time} Имя:{self.username} Сообщение: {self.message}')
#         logging.info(f'Добавили историю в файл')
#
#     async def send_password(self):
#         """Отправка пароля на сервер"""
#         password = input('Введите пароль:')
#         self.sock.sendall(pickle.dumps(['password', password]))
#         await asyncio.sleep(1.5)
#
#     async def send_name(self):
#         """Отправка имени на сервер"""
#         print('Запрос')
#         self.username = input(f"Введите имя:")
#         self.sock.sendall(pickle.dumps(["name", self.username]))
#         await asyncio.sleep(1.5)
#
#     async def welcome(self):
#         """Приветственное сообщение"""
#         self.username = self.data.split(" ")[1]
#         logging.info(f"Клиент {self.sock.getsockname()} прошел авторизацию!")
#
#     async def data_acquisition(self):
#         """Получение данных от сервера"""
#         while True:
#             try:
#                 self.data = self.sock.recv(1024)
#                 if not self.data:
#                     sys.exit(0)
#                 logging.info(f"Клиент {self.sock.getsockname()} принял "
#                              f"данные от сервера: {pickle.loads(self.data)[1]}")
#                 self.data = pickle.loads(self.data)[1]
#                 print(f"Сервер: {self.data}\n", end='')
#                 await asyncio.sleep(1)
#             except OSError:
#                 break
#
#
# async def main():
#     """
#     Ввод порта и ip сервера, валидация данных
#     """
#     IP_DEFAULT = "127.0.0.1"
#     PORT_DEFAULT = 2002
#
#     user_port = input("Введите порт (enter для значения по умолчанию):")
#     if not port_validation(user_port):
#         user_port = PORT_DEFAULT
#         print(f"Установили порт {user_port} по умолчанию!")
#
#     user_ip = input("Введите ip сервера (enter для значения по умолчанию):")
#     if not ip_validation(user_ip):
#         user_ip = IP_DEFAULT
#         print(f"Установили ip-адресс {user_ip} по умолчанию!")
#
#     client = Client(user_ip, int(user_port))
#
#
# if __name__ == "__main__":
#     main()
