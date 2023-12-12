
import protocol
import socket
import os
import logging
import glob
import shutil
import pyautogui
import subprocess
import base64

def dir_request(path):
    """
    get path
    get: path
    returns list of files
    returns: files_list
    """
    files_list = glob.glob(path+'\\*.*')
    files_list=",".join(files_list)
    return files_list


def delete_request(path):
    """
    get path to a file
    get: path
    deletes the file
    """
    os.remove(path)

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
    comment = "works"
    try:
        subprocess.call(path)
    except Exception as err:
        comment = "dosent work"
    return comment


def take_screenshot_request():
    """
    get path to a file
    get: path
    deletes the file
    """
    try:
        image = pyautogui.screenshot()
        image.save("screen.jpg")
        return "ok. taken"
    except Exception as err:
        return "couldnt take a pic"

def send_photo_request():
     """
        get path
        get: path
        returns list of files
        returns: files_list
        """

     with open("screen.jpg", "rb") as imageFile:
         comment = base64.b64encode(imageFile.read())
     comment = comment.decode()
     return comment
