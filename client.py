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

MAX_PACKET = 1024
IP = "127.0.0.1"
PORT = 1729
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'
from PIL import Image

def send_par(response,my_socket):
    print("server responded with: " + response)
    path = input("pls enter a message: ")
    my_socket.send(protocol.send_protocol(path).encode())
    response = protocol.recv_protocol(my_socket)
    return response

def check_msg(msg):
    if msg == "DIR" or msg == "DELETE" or msg == "COPY" or msg == "EXECUTE" or msg == "TAKE SCREENSHOT" or msg == "SEND PHOTO":
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
        while check_msg(msg) != True:
            print("enter one request from the options: DIR/DELETE/COPY/EXECUTE/TAKE SCREENSHOT/SEND PHOTO/EXIT")
            msg = input("pls enter a message: ")
        logging.debug("sending msg request" + msg)
        my_socket.send(protocol.send_protocol(msg).encode())
        response = protocol.recv_protocol(my_socket)
        logging.debug("getting response" + response)
        while response != "EXIT":
            if msg == "DIR" or msg == "DELETE" or msg == "EXECUTE":
                response=send_par(response,my_socket)

            elif msg == "COPY":
                response = send_par(response,my_socket)
                response = send_par(response,my_socket)

            elif msg == "SEND PHOTO":
                imgdata = base64.b64decode(response)
                filename = 'image.jpg'
                with open(filename, 'wb') as f:
                    f.write(imgdata)

                im = Image.open(filename)
                im.show()

            if (msg!="SEND PHOTO"):
                print("server responded with: " + response)

            msg = input("pls enter a message: ")
            my_socket.send(protocol.send_protocol(msg).encode())
            response = protocol.recv_protocol(my_socket)
    except socket.error as error:
        logging.error("received socket error" + str(error))
        print("socket error:" + str(error))

    finally:
        my_socket.close()


if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    assert protocol.send_protocol("message") == "0000000007message"
    assert check_msg("DIR") == True
    assert check_msg("DELETE") == True
    assert check_msg("COPY") == True
    assert check_msg("EXECUTE") == True
    assert check_msg("TAKE SCREENSHOT") == True
    assert check_msg("SEND PHOTO") == True
    assert check_msg("hh") != True

    main()
