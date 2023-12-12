"""
Author: Bar Assulin
Date: 11.12.2023
Description: server.py for cyber2.7
"""


import base64
import socket
import os
import logging
import protocol
from PIL import Image

IP = "127.0.0.1"
PORT = 1729
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'


def send_par(response, my_socket):
    """
    sending to server a parameter
    :param response: what the server asked
    :param my_socket: the socket
    :return: answer from client
    """
    print("server responded with: " + response)
    path = input("pls enter a message: ")
    logging.debug("sending path as requested" + path)
    my_socket.send(protocol.send_protocol(path).encode())
    response = protocol.recv_protocol(my_socket)
    logging.debug("getting msg request" + response)
    return response


def check_msg(msg):
    """
    check if the function exists
    :param msg: the function
    :return: if exists or not
    """
    if (msg == "DIR" or msg == "DELETE" or msg == "COPY" or msg == "EXECUTE" or msg == "TAKE SCREENSHOT" or
            "SEND PHOTO" == msg):
        return True
    else:
        return False


def main():
    """
    main
    return: the response to your request
    """
    my_socket = socket.socket()
    try:
        my_socket.connect((IP, PORT))
        msg = input("pls enter a message: ")
        while not check_msg(msg):
            print("enter one request from the options: DIR/DELETE/COPY/EXECUTE/TAKE SCREENSHOT/SEND PHOTO/EXIT")
            msg = input("pls enter a message: ")
        logging.debug("sending msg request" + msg)
        my_socket.send(protocol.send_protocol(msg).encode())
        response = protocol.recv_protocol(my_socket)
        logging.debug("getting response" + response)
        while response != "EXIT":
            if msg == "DIR" or msg == "DELETE" or msg == "EXECUTE":
                response = send_par(response, my_socket)

            elif msg == "COPY":
                response = send_par(response, my_socket)
                response = send_par(response, my_socket)

            elif msg == "SEND PHOTO":
                if response != "error":
                    imgdata = base64.b64decode(response)
                    filename = 'image.jpg'
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                    im = Image.open(filename)
                    im.show()
                else:
                    print("there is no pics. take a screenshot first")

            if msg != "SEND PHOTO":
                print("server responded with: " + response)

            msg = input("pls enter a message: ")
            logging.debug("sending msg" + msg)
            my_socket.send(protocol.send_protocol(msg).encode())
            response = protocol.recv_protocol(my_socket)
    except socket.error as error:
        logging.error("received socket error" + str(error))
        print("socket error:" + str(error))
    except KeyboardInterrupt as error:
        my_socket.send(protocol.send_protocol("EXIT").encode())
        logging.error("an error" + str(error))
        print("an error:" + str(error))
    finally:
        my_socket.close()


if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    assert protocol.send_protocol("message") == "0000000007message"
    assert check_msg("DIR")
    assert check_msg("DELETE")
    assert check_msg("COPY")
    assert check_msg("EXECUTE")
    assert check_msg("TAKE SCREENSHOT")
    assert check_msg("SEND PHOTO")
    assert not check_msg("hh")

    main()
