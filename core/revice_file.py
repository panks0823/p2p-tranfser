#!/usr/bin/env python
# -*- coding: utf-8 -*-
## 接收文件的服务端，启动时便打开端口，等待send_file进程建立连接并发送文件
## 成功接收文件后该进程就可以关闭了

import socket
import json
import struct
import os
from md5_file import GetFileMd5
from log_file import my_log

file_name=os.path.basename(__file__)
logger=my_log(file_name)

def revice_file():
    sk=socket.socket()
    sk.bind(("0.0.0.0",38080))
    sk.listen()

    conn,addr=sk.accept()
    file_len_struct=conn.recv(4)
    file_len=struct.unpack('i',file_len_struct)[0]
    file_json=conn.recv(file_len).decode()
    file=json.loads(file_json)
    logger.debug("文件%s的信息报文已接收" %file["name"])

    while True:
        with open(file['name']+"_bak", "wb") as f:
            while file['size']:
                content = conn.recv(1024)
                f.write(content)
                file['size'] -= len(content)

        if file['md5'] == GetFileMd5(file["name"]):
            conn.send('successed'.encode())
            logger.debug("文件%s已成功接收"%file["name"])
            break
        else:
            conn.send('failed'.encode())
            logger.debug("文件%s接收失败，请重发" %file["name"])
            continue

    conn.close()
    sk.close()

revice_file()
