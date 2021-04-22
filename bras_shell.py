import cmd
import configparser
import getpass
import os

import requests

import const
import utils


class BrasShell(cmd.Cmd):
    intro = "Welcome to NJU bras shell.\nType help or ? to list commands.\n"
    prompt = "(bras) "

    config_path = "./nju_bras.conf"
    parser = configparser.ConfigParser()

    username = None
    passwd = None

    def preloop(self):
        if self.load_config(self.config_path):
            self.intro += "Current user: {}\n".format(self.username)

    def show_current_user(self):
        print("Current user: {}".format(self.username))

    def load_config(self, path):
        if os.path.isfile(path):
            self.parser.read(path)
            self.username = self.parser.get("global", "username")
            self.passwd = self.parser.get("global", "passwd")
            return True
        else:
            return False

    def save_config(self):
        self.parser = configparser.ConfigParser()
        self.parser.add_section("global")
        self.parser.set("global", "username", self.username)
        self.parser.set("global", "passwd", self.passwd)
        with open(self.config_path, "w") as f:
            self.parser.write(f)

    def get_user_info(self):
        self.username = input("Username: ")
        self.passwd = getpass.getpass()

    def query_save(self):
        if utils.query_yes_no("Do you want to override?"):
            self.save_config()

    def do_load(self, path):
        if not self.load_config(path):
            print("Config file {} is not exist!")
            return
        self.show_current_user()
        if path != self.config_path:
            self.query_save()

    def do_clear(self, arg):
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)
        self.username = self.passwd = None

    def do_login(self, arg):
        s = requests.Session()
        if self.username is None or self.passwd is None:
            self.get_user_info()
            self.query_save()
        data = dict(username=self.username, password=self.passwd)
        try:
            response = s.post(const.login_url, data=data, headers=const.headers, timeout=5)
        except requests.ConnectTimeout:
            print("Connection timeout!")
            return
        reply = response.json()
        reply_code = reply["reply_code"]
        if reply_code == 1:
            print("User {} logged in successfully!".format(reply["userinfo"]["username"]))
        elif reply_code == 6:
            print("User {} has logged in!".format(reply["userinfo"]["username"]))
        elif reply_code == 3:
            print("Authentication Failed!")
            self.username = self.passwd = None
        else:
            print(reply)

    def do_logout(self, arg):
        s = requests.Session()
        try:
            response = s.post(const.logout_url, headers=const.headers, timeout=5)
        except requests.ConnectTimeout:
            print("Connection timeout!")
            return
        reply = response.json()
        reply_code = reply["reply_code"]
        if reply_code == 101:
            print("Logged out successfully!".format())
        else:
            print(reply)

    def do_show(self, arg):
        s = requests.Session()
        try:
            response_volume = s.post(const.volume_url, headers=const.headers, timeout=5)
            response_getinfo = s.post(const.getinfo_url, headers=const.headers, timeout=5)
        except requests.ConnectTimeout:
            print("Connection timeout!")
            return
        reply_volume = response_volume.json()
        reply_getinfo = response_getinfo.json()

        if reply_volume["reply_code"] != 0 or reply_getinfo["reply_code"] != 0:
            print("No user is logged in!")
            return

        username = reply_getinfo["userinfo"]["username"]
        fullname = reply_getinfo["userinfo"]["fullname"]
        service_name = reply_getinfo["userinfo"]["service_name"]
        area_name = reply_getinfo["userinfo"]["area_name"]
        balance = reply_getinfo["userinfo"]["balance"] / 100
        used_secs = reply_volume["rows"][0]["total_ipv4_volume"]
        h = used_secs // 3600
        m = used_secs % 3600 // 60

        print("Name: ", fullname)
        print("Username: ", username)
        print("Service: ", service_name)
        print("Area: ", area_name)
        print("Balance: {:.2f}".format(balance))
        print("Used time: {}h{}m".format(h, m))

    def do_user(self, arg):
        if self.username is None:
            print("Username is unset!")
            return
        self.show_current_user()

    def do_exit(self, arg):
        return True

    do_EOF = do_exit
