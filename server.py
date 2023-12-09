"""
Author: Bar Assulin
Date: 19.11.2023
Description: server.py for cyber2.6
"""
import protocol
import socket
import os
import logging
import glob
import shutil
import pyautogui
import subprocess

QUEUE_LEN = 1
MAX_PACKET = 1024
NAME = "need to get from client"
NAME2= "need to get from client,name of file"
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'

def recv_protocol(message):

    """
        while protocol.recive_protocol(message):
        message = client_socket.recv(MAX_PACKET).decode()
        message=message[2:]
    """

    return message

def dir_request(path):
    """
    get path
    get: path
    returns list of files
    returns: files_list
    """
    files_list = glob.glob(r''+path+'*.*')
    return files_list


def delete_request(path):
    """
    get path to a file
    get: path
    deletes the file
    """
    os.remove(r'' +path+'.txt')



def copy_request(C1,C2):
    """
    get path to a file and to the place the client wants to copy the file in to
    get: C1,C2
    copys the file (from C1) to another place (C2)
    """
    shutil.copy(r''+C1, r''+C2)


def execute_request(path):
    """
    get path
    get: path
    returns list of files
    returns: files_list
    """
    subprocess.call(r''+path+'.exe')
    """need to return if works or not"""
    return files_list


def take_screenshot_request():
    """
    get path to a file
    get: path
    deletes the file
    """
    image = pyautogui.screenshot()
    image.save(r'screen.jpg')


def send_photo_request():
     """
        get path
        get: path
        returns list of files
        returns: files_list
        """
     with open("filepath/filename", "rb") as f:
         image=f.read()
     return image


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
                request = client_socket.recv(MAX_PACKET).decode()
                recv_protocol(request)
                logging.debug("getting request" + request)
                while request != "EXIT":
                    if request == "DIR":
                        client_socket.send(protocol.send_protocol("enter path").encode())
                        path = client_socket.recv(MAX_PACKET).decode()
                        recv_protocol(path)
                        comment = dir_request(path)
                    elif request == "DELETE":
                        client_socket.send(protocol.send_protocol("enter path").encode())
                        path = client_socket.recv(MAX_PACKET).decode()
                        recv_protocol(path)
                        delete_request(path)
                        comment = "ok. deleted"
                    elif request == "COPY":
                        client_socket.send(protocol.send_protocol("enter path you want too copy from").encode())
                        path_to_copy = client_socket.recv(MAX_PACKET).decode()
                        recv_protocol(path_to_copy)
                        client_socket.send(protocol.send_protocol("enter path you want too copy in to").encode())
                        path_to_paste = client_socket.recv(MAX_PACKET).decode()
                        recv_protocol(path_to_paste)
                        copy_request(path_to_copy,path_to_paste)
                        comment = "ok. coppied"
                    elif request == "EXECUTE":
                        client_socket.send(protocol.send_protocol("enter path").encode())
                        path = client_socket.recv(MAX_PACKET).decode()
                        recv_protocol(path)
                        comment = execute_request(path)
                    elif request == "TAKE SCREENSHOT":
                        take_screenshot_request()
                        comment = "ok. taken"
                    elif request == "SEND PHOTO":
                        comment = send_photo_request()
                    else:
                        comment = "enter one request from the options: DIR/DELETE/COPY/EXECUTE/TAKE SCREENSHOT/SEND PHOTO/EXIT"

                    logging.debug("sending comment" + comment)
                    client_socket.send(protocol.send_protocol(comment).encode())
                    request = client_socket.recv(MAX_PACKET).decode()
                    recv_protocol(request)
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

    main()
