import argparse
import copy
import json
from getpass import getpass

import requests
from colorama import Back, Fore, Style, init

from lib import auth, lotto645


def login(user_id: str, user_pw: str):
    globalAuthCtrl = auth.AuthController()
    globalAuthCtrl.login(user_id, user_pw)

    return globalAuthCtrl


def buy_lotto645(authCtrl: auth.AuthController, cnt: int, mode: str):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    lotto.buy_lotto645(authCtrl, cnt, _mode)


def loggerSetup():
    # init(autoreset=True)
    init()
    print(Fore.GREEN + Style.BRIGHT + "DongHaeng Lottery CLI is working...")


def set_argparse():
    parser = argparse.ArgumentParser(description="동행복권 비공식 API")

    parser.add_argument(
        "-u",
        "--username",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--password",
        required=True,
    )
    parser.add_argument("-C", "--category", required=True, choices=["lotto645"])
    parser.add_argument("-t", "--task", required=True, choices=["buy"])
    parser.add_argument(
        "-c",
        "--count",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        choices=["auto"],
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # loggerSetup()

    args = set_argparse()

    print(args)

    if args.category == "lotto645":
        authCtrl = login(args.username, args.password)
        buy_lotto645(authCtrl, args.count, args.mode)
    exit(0)
