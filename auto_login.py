import configparser
import os
import time

import requests

import const
import utils


def login(username, passwd):
    print("Trying to login... " + utils.get_time_str())
    data = dict(username=username, password=passwd)
    s = requests.Session()
    response = s.post(const.login_url, data=data, headers=const.headers, timeout=5)
    reply = response.json()
    reply_code = reply["reply_code"]

    if reply_code == 1:
        print("User {} logged in successfully!".format(reply["userinfo"]["username"]))
    elif reply_code == 6:
        print("User {} has logged in!".format(reply["userinfo"]["username"]))
    elif reply_code == 3:
        print("Authentication Failed!")
    else:
        print(reply)


def main():
    parser = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    parser.read("./nju_bras.conf")
    username = parser.get("global", "username")
    passwd = parser.get("global", "passwd")

    while True:
        login(username, passwd)
        time.sleep(60 * 5)


if __name__ == '__main__':
    main()
