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
    #将接收文件的主机dest和要被发送的文件big_file组成命令,发送给接收命令的主机src(也就是要发送文件的主机)
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
#lst1中存放已准备发送文件的服务器列表
f=open('../conf/config','r')
dict1=json.load(f)
(big_file, lst2), = dict1.items()
#lst2中存放准备接收文件的服务器列表

t_lst=[]

while len(lst2) != 0:
    # 直到lst2为空，否则不断循环执行以下部分,利用t_lst列表完成一次while循环需要等待一次中所有线程结束
    # 根据lst1的元素数量n，启动n个线程同时执行send_cmd(src,dest)
    for i in range(0,len(lst1)):
        if i< len(lst2):
            logger.debug("由源主机%s向目标主机%s发送文件..." %(lst1[i],lst2[i]))
            # send_cmd(lst1[i],lst2[i])
            t = Thread(target=send_cmd, args=(lst1[i],lst2[i],big_file))
            t_lst.append(t)
            t.start()
        else:
            break
            #当取到lst1中的服务器索引数值超过lst2长度则表示已经没有准备结束文件的服务器了
    for t in t_lst:
        t.join()
