#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import os
from send_file import send_file
from threading import Thread
from log_file import my_log

file_name=os.path.basename(__file__)
logger=my_log(file_name)
## 接收命令的服务端，启动时便打开端口等待接收send_cmd发来的命令，以子线程接收命令
## 从命令中获取目标主机名1和目标文件名1，接着调用send_file中的send函数，才知道要发什么文件给谁。
## 主进程永久存活着等着下一次接受send_cmd发来的命令

def revice_cmd(sk):
    logger.debug("等待接收命令")
    conn, addr = sk.accept()
    cmd_json = conn.recv(1024).decode()
    cmd = json.loads(cmd_json)
    logger.debug("收到命令:向主机%s传送文件%s"%(cmd[0], cmd[1]))

    cmd_status = send_file(cmd[0], cmd[1],cmd[2])
    logger.debug("命令执行状态：%s"%cmd_status)
    conn.send(cmd_status.encode())
    conn.close()

sk = socket.socket()
sk.bind(("0.0.0.0", 38070))
sk.listen()

while True:
    t=Thread(target=revice_cmd,args=(sk,))
    t.start()
    t.join()

