import socket
import threading
from concurrent.futures import ThreadPoolExecutor

HOST = '127.0.0.1'
PORT = 8000


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server_socket = None
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.is_running = False

    def start(self) -> None:
        """
        Start the server.
        """
        # Create a new server socket on the specified address and port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow the socket to accept new connections without blocking
        self.server_socket.setblocking(0)

        self.server_socket.bind((self.host, self.port))
        print(f"Server started on {self.host}:{self.port}")

        self.server_socket.listen()

        # Set the server running flag to True
        self.is_running = True

        while self.is_running:
            try:
                # Wait for a client to connect
                client_socket, client_address = self.server_socket.accept()

                # Add the task to the thread pool
                self.executor.submit(self.receive_from_client, client_socket, client_address)
            except OSError:
                # If there are no new connections to accept, continue the loop
                continue

    def receive_from_client(self, client_socket, client_address) -> None:
        """
        Handle data received from a client.
        """
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                print(f"Received {len(data)} bytes from {client_address}")

                try:
                    client_socket.sendall(data)
                    print(f"Sent {len(data)} bytes back to {client_address}")
                except socket.error as e:
                    print(f"Error occurred while sending data to {client_address}: {e}")
                    break

        print(f"{client_address} disconnected")

    def stop(self) -> None:
        """
        Stop the server.
        """
        self.is_running = False

        if self.server_socket is not None:
            self.server_socket.close()

        self.executor.shutdown()
        print("Server stopped")


if __name__ == "__main__":
    server = Server(host=HOST, port=PORT)
    server.start()

# import socket
# import threading
# from concurrent.futures import ThreadPoolExecutor
#
#
# HOST = '127.0.0.1'
# PORT = 8001
#
#
# class Server:
#     def __init__(self, host: str, port: int) -> None:
#         self.host = host
#         self.port = port
#         self.server_socket = None
#         self.executor = ThreadPoolExecutor(max_workers=10)
#         self.is_running = False
#
#     def start(self) -> None:
#         """
#         Запуск сервера.
#         """
#         # Создаем новый серверный сокет на указанном адресе и порту
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind((self.host, self.port))
#
#         # Выводим сообщение о запуске сервера
#         print(f"Server started on {self.host}:{self.port}")
#
#         # Начинаем прослушивание на созданном серверном сокете
#         self.server_socket.listen()
#
#         # Устанавливаем флаг работы сервера в True
#         self.is_running = True
#
#         while self.is_running:
#             # Ожидаем подключения клиента
#             client_socket, client_address = self.server_socket.accept()
#
#             # Выводим сообщение о подключению клиента
#             print(f"Client connected from {client_address[0]}:{client_address[1]}")
#
#             # Добавляем задачу для выполнения в пул потоков
#             self.executor.submit(self.receive_from_client, client_socket)
#
#     def receive_from_client(self, client_socket) -> None:
#         """
#         Обработка данных от клиента.
#         """
#         with client_socket:
#             while True:
#                 # Получаем данные от клиента (порциями по 1 КБ)
#                 data = client_socket.recv(1024)
#
#                 # Если нет данных, то клиент закрыл соединение
#                 if not data:
#                     break
#
#                 # Выводим сообщение о приеме данных от клиента
#                 print(f"Received {len(data)} bytes from the client")
#
#                 # Отправляем данные обратно клиенту
#                 try:
#                     client_socket.sendall(data)
#                     print(f"Sent {len(data)} bytes back to the client")
#                 except socket.error as e:
#                     print(f"Error occurred while sending data: {e}")
#                     break
#
#         # Выводим сообщение об отключении клиента
#         print("Client disconnected")
#
#
#
#     def stop(self) -> None:
#         """
#         Остановка сервера.
#         """
#         # Устанавливаем флаг работы сервера в False
#         self.is_running = False
#
#         # Закрываем серверный сокет
#         if self.server_socket is not None:
#             self.server_socket.close()
#
#         # Ожидаем завершения всех задач в пуле потоков
#         self.executor.shutdown()
#
#         # Выводим сообщение об остановке сервера
#         print("Server stopped")
#
#
# if __name__ == "__main__":
#     server = Server(host=HOST, port=PORT)
#     server.start()
