#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

host = "127.0.0.1"
port = 10001

# 
if __name__ == '__main__':
    # processingのコードとsocket通信
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_DGRAMでUDP通信の方がいいかも
    socket_client.connect((host, port))

    for i in range(360):  # 360フレーム分のデータを送信して回転
        # データを送信
        message = f"{1}\n"  # 回転速度を1として送信
        socket_client.send(message.encode('utf-8'))
        time.sleep(0.05)  # 0.05秒ごとに送信

    socket_client.close()
