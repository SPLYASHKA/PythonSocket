import socket
import pygame
import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(('localhost', 9090))
main_socket.setblocking(0)
main_socket.listen(2)

players_sockets = []
clock = pygame.time.Clock()

framerate = 60
while True:
    # Проверка желающих подключиться
    try:
        new_socket, addr = main_socket.accept()
        print("Подключился ", addr)
        new_socket.setblocking(0)
        players_sockets.append(new_socket)
    except:
        print("Нет желающих")
        pass

    # Считываем посылки клиентов
    sum_of_data = 0
    for sock in players_sockets:
        try:
            data = sock.recv(1024)
            data = data.decode()
            for x in data.split('>'):
                sum_of_data += int(x)
        except:
            pass
    print(sum_of_data)
    # отправка нового состояния
    for sock in players_sockets:
        try:
            message = str(sum_of_data) + '>'
            sock.send(message.encode())
        except:
            players_sockets.remove(sock)
            sock.close()
            print('Отключился игрок')

    # clock.tick(framerate)
    time.sleep(1)
# if __name__ == '__main__':
#     print("bebra")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
