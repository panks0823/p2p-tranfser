#!/bin/bash

cd ../core/

if [ $1 == master ];then
    nohup python3 ../core/revice_cmd.py &
    nohup python3 ../core/send_cmd.py &

elif [ $1 == node2 ];then
    nohup python3 ../core/revice_cmd.py &
    nohup python3 ../core/revice_file.py &

elif [ $1 == stop ];then
    ps -ef | grep python3|grep revice_|grep -v grep | awk '{print $2}'| xargs kill -9
fi