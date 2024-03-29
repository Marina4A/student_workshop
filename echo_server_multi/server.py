import socket
import hashlib
import json
import pickle
from threading import Thread
import logging
from time import sleep

from validation import free_port, port_validation

logging.basicConfig(format='%(asctime)s {%(levelname)s %(funcName)s: %(message)s}',
                    handlers=[logging.FileHandler('log/server.log', encoding='utf-8'), logging.StreamHandler()],
                    level=logging.INFO)


class Server:
    def __init__(self, ip, port):
        """
        :param
            port: порт сервера
        """
        self.port = port
        self.users_authorization = []
        self.clients = []
        self.users = 'users.json'
        self.status = None
        self.ip = ip
        self.server_run()

    def server_run(self):
        """
        Запуск сервера
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(5)
        self.sock = sock
        logging.info(f'Сервер запущен! Порт {self.port}.')
        while True:
            conn, addr = self.sock.accept()
            Thread(target=self.listen_client, args=(conn, addr)).start()
            sleep(1)
            logging.info(f"Подключился клиент {addr}")
            self.clients.append(conn)

    def listen_client(self, conn, address):
        """
        Отправка сообщения клиента, либо закрытие соединения
        Args:
            conn (socket): сокет с данными клиента
            address (tuple): ip-адрес и номера соединения
        """
        self.authorization(address, conn)
        while True:
            try:
                data = conn.recv(1024)
            except ConnectionRefusedError:
                conn.close()
                self.clients.remove(conn)
                logging.info(f'Отключение клиента {address}!')
                break

            if data:
                status, data, username = pickle.loads(data)
                logging.info(f"Прием данных от клиента '{username}_{address[1]}': {data}")
                self.broadcast(data, conn, address, username)

            else:
                # Закрываем соединение
                conn.close()
                self.clients.remove(conn)
                logging.info(f"Отключение клиента {address}!")
                break

    # def authorize_user(self, address, conn):
    #     name_user = None
    #
    #     try:
    #         self.users_authorization = self.read_json()
    #         logging.debug(f'users_authorization: {self.users_authorization=}')
    #
    #         # Get user data based on IP address
    #         user_data = self.users_authorization.get(address[0])
    #         if user_data:
    #             conn.sendall(pickle.dumps(["passwd", "запрашивает имя"]))
    #             name_user = pickle.loads(conn.recv(1024))[1]
    #
    #             found_user = any(user for user in user_data if self.check_name(user['name'], name_user))
    #             if found_user:
    #                 logging.debug(f'User {name_user} has been found')
    #
    #                 while True:
    #                     conn.sendall(pickle.dumps(["passwd", "запрашивает пароль"]))
    #                     passwd = pickle.loads(conn.recv(1024))[1]
    #
    #                     if self.check_password(passwd, user['password']):
    #                         logging.info(f'Password "{passwd}" correct!')
    #                         conn.sendall(pickle.dumps(["success", f"Приветствую, {name_user}"]))
    #                         break
    #                     else:
    #                         conn.sendall(pickle.dumps(["passwd", "пароль не верный"]))
    #             else:
    #                 raise ValueError
    #         else:
    #             raise ValueError
    #
    #     except json.decoder.JSONDecodeError as err:
    #         logging.error(f'Unable to decode JSON: {err}')
    #         self.registration(address, conn, name_user)
    #
    #     except ValueError as err:
    #         logging.error(f'Error occurred: {err}')
    #         self.registration(address, conn, name_user)

    def authorization(self, address, conn):
        """
        Авторизация пользователя на сервере
        :param address: IP-адрес и номер соединения
        :param conn: сокет
        """

        name_user = None

        try:
            self.users_authorization = self.read_json()
            print(f'{self.users_authorization=}')
            for values in self.users_authorization:
                print(f'{values=}')
                if address[0] in values:
                    conn.sendall(pickle.dumps(["passwd", "запрашивает имя"]))
                    name_user = pickle.loads(conn.recv(1024))[1]
                    for user in values[address[0]]:
                        if self.check_name(user['name'], name_user):
                            print(f'Пользователь {name_user} найден')
                        else:
                            raise ValueError
                        while True:
                            conn.sendall(pickle.dumps(["passwd", "запрашивает пароль"]))
                            passwd = pickle.loads(conn.recv(1024))[1]

                            if self.check_password(passwd, user['password']):
                                print('Пароль верный')
                                logging.info(f'Пароль "{passwd}" верный!')
                                conn.sendall(pickle.dumps(["success", f"Приветствую, {name_user}"]))

                                break
                            else:
                                conn.sendall(pickle.dumps(["passwd", "пароль не верный"]))
                else:
                    raise ValueError
        except (json.decoder.JSONDecodeError, ValueError):
            self.registration(address, conn, name_user)

    def broadcast(self, messenger, conn, address, username):
        """
        Отправка данных клиенту (сообщение и имя пользователя с номером соединения)
        :param messenger: сообщение
        :param conn: сокет с данными
        :param address: ip-адрес и номер соединения
        :param username: имя клиента
        """
        username += f"_{address[1]}"
        for sock in self.clients:
            if sock == conn:
                data = pickle.dumps(["message", messenger, username])
                sock.sendall(data)
                logging.info(f"Отправляем данные клиенту {sock.getsockname()}: {messenger}")

    def read_json(self):
        """Чтение файла с авторизованными пользователями"""
        with open(self.users, 'r', encoding='utf-8') as file:
            users_text = json.load(file)
        return users_text

    def registration(self, address, conn, name):
        """
        Регистрация новых пользователей
        и добавление информации о них в json файл
        Args:
            :param address: IP-адрес и номер соединения
            :param conn: сокет
        """
        conn.sendall(pickle.dumps(["passwd", "Регистрация нового пользователя"]))
        if name is None:
            conn.sendall(pickle.dumps(["name", "запрашивает имя"]))
            name = pickle.loads(conn.recv(1024))[1]
        conn.sendall(pickle.dumps(["password", "запрашивает пароль"]))
        password = self.hash_generation(pickle.loads(conn.recv(1024))[1])
        conn.sendall(pickle.dumps(["success", f"Приветствую, {name}"]))
        print(address, name, password)
        for index, addr in enumerate(self.users_authorization):
            if addr == address[0]:
                self.users_authorization[index].append([{'name': name, 'password': password}])
                break
        else:
            self.users_authorization.append({address[0]:[{'name': name, 'password': password}]})

        self.write_json()
        self.users_authorization = self.read_json()

    def write_json(self):
        """
        Запись пользователей в json-файл
        """
        with open(self.users, 'w', encoding='utf-8') as file:
            json.dump(self.users_authorization, file, indent=4)

    def check_password(self, password, userpassword):
        """
        Проверяем пароль из файла и введенный пользователем
        Args:
            :param password: введенный пароль пользователем
            :param userpassword: пароль пользователя из json
        returns:
            boolean: True/False
        """
        key = hashlib.md5(password.encode() + b'salt').hexdigest()
        print(key, userpassword)
        return key == userpassword

    def check_name(self, name, username):
        """
        Сравниваем логин из json с введенным пользователем
        :param name: данные из json-файла
        :param username: введенный логин пользователем
        :return:
            boolean: True/False
        """
        return name == username

    def hash_generation(self, password):
        """
        Генерация пароля
        Args:
            password: пароль
        returns:
            str: хэш пароль
        """

        key = hashlib.md5(password.encode() + b'salt').hexdigest()
        return key


def main():
    """
    Проверка корректности порта
    Запуск сервера
    """
    port = 2001
    IP = "127.0.0.1"
    if not port_validation(port):
        if not free_port(port):
            port_free = False
            while not port_free:
                port += 1
                port_free = free_port(port)
    try:
        server = Server(IP, port)
    except KeyboardInterrupt:
        logging.info('Сервер остановился!')


if __name__ == '__main__':
    main()
