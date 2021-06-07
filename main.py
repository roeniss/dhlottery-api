import copy
import json
from getpass import getpass

import requests

from lib import auth, lotto645

globalAuthCtrl = None


def login():
    global globalAuthCtrl
    globalAuthCtrl = auth.AuthController()
    print(globalAuthCtrl)
    _id = input("ID : ")
    _pw = getpass("Password : ")
    globalAuthCtrl.login(_id, _pw)


def buyLotto645():
    print(globalAuthCtrl)
    _cnt = int(input("How many (1 ~ 5) : "))
    _mode = input("Mode (auto, manual) : ")
    lotto = lotto645.Lotto645()
    lotto.buyLotto645(globalAuthCtrl, _cnt, _mode)


if __name__ == "__main__":
    # while 1:
    #     cmd = input("Command (login, buyLotto645, quit) : ")
    #     if cmd == "login":
    #         login()
    #     elif cmd == "buyLotto645":
    #         buyLotto645()
    #     elif cmd == "quit":
    #         exit(0)
    login()
    buyLotto645()
