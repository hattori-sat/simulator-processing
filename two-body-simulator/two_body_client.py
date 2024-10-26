#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import socket
import time

# サーバー設定
host = "127.0.0.1"  
port = 10001        

# 衛星のクラス
class SimulatorObject:
    def __init__(self, position, velocity):
        """インスタンスが作成されたときに呼ばれる関数"""
        self.position = np.matrix(position, dtype=float)  # 2次元位置
        self.velocity = np.matrix(velocity, dtype=float)  # 2次元速度
        self.time_history = [0]
        self.position_history = [self.position.copy()]  # 位置の履歴
        self.velocity_history = [self.velocity.copy()]  # 速度の履歴
        
        # シミュレーションに使う変数をここで定義します
        self.mass1 = 10  # 物体1の質量
        self.mass2 = 10  # 物体2の質量
        self.force = 0   # 外力

    def rk4(self, h, t):
        """4次のルンゲクッタ法による位置・速度の更新"""
        k1_pos = self.velocity.copy()
        k1_vel = self.acceleration(self.position, t)

        k2_pos = self.velocity + k1_vel * (h / 2)
        k2_vel = self.acceleration(self.position + k1_pos * (h / 2), t + (h / 2))

        k3_pos = self.velocity + k2_vel * (h / 2)
        k3_vel = self.acceleration(self.position + k2_pos * (h / 2), t + (h / 2))

        k4_pos = self.velocity + k3_vel * h
        k4_vel = self.acceleration(self.position + k3_pos * h, t + h)

        # 更新された位置と速度
        self.position += h / 6 * (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos)
        self.velocity += h / 6 * (k1_vel + 2 * k2_vel + 2 * k3_vel + k4_vel)

        # 履歴に追加
        self.time_history.append(t)
        self.position_history.append(self.position.copy())
        self.velocity_history.append(self.velocity.copy())

    def acceleration(self, position, t):
        """加速度の計算: シンプルな2次元重力を適用"""
        G = 1.0  # 重力定数のスケーリング係数
        central_mass = 1.0  # 中心の天体の質量

        # 中心の位置（原点）からの距離ベクトル
        r_vector = -position
        r = np.linalg.norm(r_vector)
        if r == 0:
            return np.matrix([0.0, 0.0]).T  # ゼロ割りを避ける

        # 重力による加速度
        gravity_acc = G * central_mass / r**2 * (r_vector / r)
        
        # 外力による加速度（必要に応じて変更）
        tension_acc = np.matrix([0.0, 0.0]).T  # ここは外力を加える場合に変更

        return gravity_acc + tension_acc

    def set_force(self, force):
        """外力を設定するメソッド"""
        self.force = force

# ソケット通信でデータを送信
def send_position_data(socket_client, position1, position2):
    """2つのオブジェクトの位置データをソケットを介して送信するメソッド"""
    message = f"{position1[0, 0]},{position1[0, 1]},{position2[0, 0]},{position2[0, 1]}\n"
    socket_client.send(message.encode('utf-8'))

# メイン処理
if __name__ == '__main__':
    # ソケット設定
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((host, port))

    # シミュレーションオブジェクトの作成
    object1 = SimulatorObject(position=[100.0, 0.0], velocity=[0.0, 0.5])
    object2 = SimulatorObject(position=[-100.0, 0.0], velocity=[0.0, -0.5])

    # シミュレーションパラメータ
    h = 0.01  # タイムステップ
    total_time = 50  # 総シミュレーション時間
    steps = int(total_time / h)

    # シミュレーションループ
    for step in range(steps):
        t = step * h
        object1.rk4(h, t)
        object2.rk4(h, t)

        # 位置データを送信
        send_position_data(socket_client, object1.position, object2.position)

        # データ送信の間隔を設定
        time.sleep(h)

    # ソケット通信を終了
    socket_client.close()
