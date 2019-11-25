#!/usr/bin/env python
# -*- coding: utf-8 -*-
## 发生文件的客户端
## 被revice_cmd程序中的子线程调用，获取参数主机名1和文件名1，然后向主机名1发送文件名1
## 文件发送成功后返回success给revice_cmd程序
import socket
import os
import json
import struct
from md5_file import GetFileMd5
from log_file import my_log

file_name=os.path.basename(__file__)
logger=my_log(file_name)

def send_file(host_name,file_name):

    ck=socket.socket()
    ck.connect((host_name,38080))
    file={}
    file["name"] = file_name
    file["size"] = os.path.getsize(file_name)
    file['md5'] = GetFileMd5(file_name)
    file_json=json.dumps(file)
    file_len_struct=struct.pack('i',len(file_json))
    ck.send(file_len_struct)
    ck.send(file_json.encode())
    logger.debug("文件%s的信息报文构建并已发送"%file_name)

    while True:
        with open(file['name'], "rb") as f:
            while file['size']:
                content = f.read(1024)
                ck.send(content)
                file['size'] -= len(content)

        send_status=ck.recv(1024).decode()
        if send_status == 'successed':
            logger.debug("文件%s已成功发送" % file["name"])
            break
        else:
            logger.debug("文件%s发送失败，准备重发" % file["name"])
            continue

    return "success"
