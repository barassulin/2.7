"""
Author: Bar Assulin
Date: 11.12.2023
Description: server.py for cyber2.7
"""


def send_protocol(message):
    """
    send a string with her length
    :param message: the string
    :return: a string with her length
    """
    length = str(len(message))
    zfill_length = length.zfill(10)
    message = zfill_length + message
    return message


def recv_protocol(socket):
    """
    get from socket the length of the string and the string
    :param socket: the socket
    :return: the string
    """
    length = socket.recv(10).decode()
    message = socket.recv(int(length)).decode()
    return message
