import copy
import json
from getpass import getpass

import requests
from colorama import Back, Fore, Style, init

from lib import auth, lotto645

globalAuthCtrl = None


def login():
    global globalAuthCtrl
    if globalAuthCtrl != None:
        print("You are already logged in")
    globalAuthCtrl = auth.AuthController()
    _id = input("ID : ")
    _pw = getpass("Password : ")
    globalAuthCtrl.login(_id, _pw)


def buy_lotto645():
    _cnt = int(input("How many (1 ~ 5) : "))
    _mode = input("Mode (auto, manual) : ")
    lotto = lotto645.Lotto645()
    lotto.buy_lotto645(globalAuthCtrl, _cnt, _mode)


def loggerSetup():
    # init(autoreset=True)
    init()
    print(Fore.GREEN + Style.BRIGHT + "DongHaeng Lottery CLI is working...")


if __name__ == "__main__":
    loggerSetup()

    # testing...
    login()
    buy_lotto645()
    exit(0)
    # ...testing

    while 1:
        cmd = input("Command (login, buy_lotto645, quit) : ")
        if cmd == "login":
            login()
        elif cmd == "buy_lotto645":
            buy_lotto645()
        elif cmd == "quit":
            exit(0)
