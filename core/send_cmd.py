#!/usr/bin/env python
# -*- coding: utf-8 -*-

## 发送命令的服务端，向各主机中的revice_cmd进程发送命令，告知其目标主机名1和目标文件名1
import socket
import json
import os
from threading import Thread
from log_file import my_log

file_name=os.path.basename(__file__)
logger=my_log(file_name)

def send_cmd(src,dest,big_file):
    ##  需要知道接收命令的主机(也是调用发送文件的主机src)和接收文件的主机dest
    ck = socket.socket()
    ck.connect((src, 38070))

    cmd=[dest,big_file]
    cmd_json=json.dumps(cmd)
    ck.send(cmd_json.encode())
    status=ck.recv(1024)
    logger.debug("由源主机%s向目标主机%s发送文件成功" %(src,dest))
    new = dest
    lst1.append(new)
    lst2.remove(new)


lst1=['127.0.0.1']
f=open('../conf/config','r')
dict1=json.load(f)
(big_file, lst2), = dict1.items()

t_lst=[]
##直到list2为空，否则不断循环执行以下部分
    ##根据list1的元素数量n，启动n个线程同时执行send_cmd(src,dest)

while len(lst2) != 0:
    for i in range(0,len(lst1)):
        if i< len(lst2):
            logger.debug("由源主机%s向目标主机%s发送文件..." %(lst1[i],lst2[i]))
            # send_cmd(lst1[i],lst2[i])
            t = Thread(target=send_cmd, args=(lst1[i],lst2[i],big_file))
            t_lst.append(t)
            t.start()
        else:
            break
    for t in t_lst:
        t.join()
