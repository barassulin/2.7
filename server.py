"""
Author: Bar Assulin
Date: 11.12.2023
Description: server.py for cyber2.7
"""


import protocol
import socket
import os
import logging
import shutil
import func

QUEUE_LEN = 1
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


def get_par(client_socket, string):
    """
    gets a parameter
    :param client_socket: the socket
    :param string: what to send to the client
    :return: the response from the client
    """
    client_socket.send(protocol.send_protocol(string).encode())
    logging.debug("sending msg request" + string)
    par = protocol.recv_protocol(client_socket)
    logging.debug("getting parameter " + par)
    return par


def check_par_file(par):
    """
    check if the file exists
    :param par: path to a file
    :return: the path or "error" if dosent exists
    """
    if not os.path.isfile(par):
        par = "error"
    return par


def check_par_dir(par):
    """
    check if the dir exists
    :param par: path to a dir
    :return: the path or "error" if dosent exists
    """
    if not os.path.isdir(par):
        par = "error"
    return par


def main():
    """
    main
    return: response to a request from a client
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        my_socket.bind(('0.0.0.0', 1729))
        my_socket.listen(QUEUE_LEN)
        while True:
            client_socket, client_address = my_socket.accept()
            try:
                request = protocol.recv_protocol(client_socket)
                logging.debug("getting request" + request)
                while request != "EXIT":
                    if request == "DIR":
                        path = get_par(client_socket, "enter path")
                        path = check_par_dir(path)
                        if path == "error":
                            comment = "error, the path does not exist"
                        else:
                            comment = func.dir_request(path)

                    elif request == "DELETE":
                        path = get_par(client_socket, "enter path")
                        path = check_par_file(path)
                        if path == "error":
                            comment = "error, the path does not exist"
                        else:
                            func.delete_request(path)
                            comment = "ok. deleted"

                    elif request == "COPY":
                        path_to_copy = get_par(client_socket, "enter path you want too copy from")
                        path_to_copy = check_par_file(path_to_copy)
                        path_to_paste = get_par(client_socket, "enter path you want too copy in to")
                        path_to_paste = check_par_dir(path_to_paste)
                        if path_to_paste == "error" or path_to_copy == "error":
                            comment = "error, the path does not exist"
                        else:
                            func.copy_request(path_to_copy, path_to_paste)
                            comment = "ok. coppied"

                    elif request == "EXECUTE":
                        path = get_par(client_socket, "enter path")
                        comment = func.execute_request(path)

                    elif request == "TAKE SCREENSHOT":
                        comment = func.take_screenshot_request()

                    elif request == "SEND PHOTO":
                        comment = func.send_photo_request()

                    else:
                        comment = ("enter one request from the options: DIR/DELETE/COPY/EXECUTE/TAKE SCREENSHOT/SEND "
                                   "PHOTO/EXIT")

                    logging.debug("sending comment" + comment)
                    client_socket.send(protocol.send_protocol(comment).encode())
                    request = protocol.recv_protocol(client_socket)
                    logging.debug("getting request" + request)

            except socket.error as err:
                logging.error("received socket error on client socket" + str(err))
                print('received socket error on client socket' + str(err))

            finally:
                msg = "EXIT"
                try:
                    client_socket.send(protocol.send_protocol(msg).encode())
                except socket.error as err:
                    logging.error("couldn't disconnect properly" + str(err))
                client_socket.close()
    except socket.error as err:
        logging.error("received socket error on server socket" + str(err))
        print('received socket error on server socket' + str(err))

    finally:
        my_socket.close()


if __name__ == "__main__":
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    assert protocol.send_protocol("message") == "0000000007message"

    os.makedirs(r"C:\Cyber check 2.7 new")
    os.makedirs(r"C:\Cyber check 2 2.7 new")
    with open(r'C:\Cyber check 2.7 new\demofile1.txt', 'a') as fp:
        fp.write('This is first line')
        pass
    with open(r'C:\Cyber check 2.7 new\demofile2.txt', 'a') as fp:
        pass

    filepath = r"C:\Cyber check 2.7 new\demofile2.txt"

    assert func.dir_request(
        r"C:\Cyber check 2.7 new") == r'C:\Cyber check 2.7 new\demofile1.txt,C:\Cyber check 2.7 new\demofile2.txt'

    if os.path.isfile(filepath):
        func.delete_request(r"C:\Cyber check 2.7 new\demofile2.txt")
    assert not os.path.isfile(filepath)

    filepath = r"C:\Cyber check 2.7 new\demofile1.txt"
    filepath2 = r"C:\Cyber check 2 2.7 new\demofile1.txt"
    if not os.path.isfile(filepath2):
        func.copy_request(filepath, r"C:\Cyber check 2 2.7 new")
    assert os.path.isfile(filepath2)

    if not os.path.isfile("screen.jpg"):
        func.take_screenshot_request()
    assert os.path.isfile("screen.jpg")
    func.delete_request("screen.jpg")
    shutil.rmtree(r"C:\Cyber check 2.7 new")
    shutil.rmtree(r"C:\Cyber check 2 2.7 new")

    main()
