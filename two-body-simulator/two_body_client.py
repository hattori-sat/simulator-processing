#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import socket
import time
import matplotlib.pyplot as plt

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
        
        # シミュレーションに使うパラメータ
        # ここでは適当な値を設定しておきましょう。その後、メソッドとしてset_xxxを追加しましょう
        self.mass = 10  # 物体の質量
        self.force = np.matrix([0,0], dtype=float)  # 外力

    def rk4(self, h, t):
        """4次のルンゲクッタ法による位置・速度の更新"""
        k1_pos = self.velocity.copy()
        k1_vel = self.acceleration(self.position, t).copy()

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

    # 運動方程式はここに記載しましょう
    # ma = f を a = f / m として、その形で書きましょう
    def acceleration(self, position, t):
        """加速度=の形にしましょう"""
        acc = self.force / self.mass
        return acc

    def set_force(self, force):
        """外力を設定するメソッド"""
        self.force = np.matrix(force, dtype=float)  # 外力
        
    def set_mass(self,mass):
        """質量[kg]を設定するメソッド"""
        self.mass = mass  # 物体の質量
    
    def plot_trajectory(self, filename="trajectory.png"):
        """位置の履歴をグラフにプロットし、画像として保存するメソッド"""
        positions = np.array(self.position_history)  # 位置履歴をNumPy配列に変換
        positions = positions.reshape(-1, 2)  # 位置データを (N, 2) の形に整形
        times = np.array(self.time_history)  # 時間履歴をNumPy配列に変換
        plt.figure(figsize=(10, 5))
        plt.plot(times, positions[:, 0], label='X Position', color='blue')  # X位置
        # plt.plot(times, positions[:, 1], label='Y Position', color='red')   # Y位置
        plt.title('Trajectory of the Simulator Object')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.legend()
        plt.grid()
        plt.savefig(filename)  # 画像として保存
        plt.close()  # プロットを閉じる

    def plot_velocity(self, filename="velocity.png"):
        """速度の履歴をグラフにプロットし、画像として保存するメソッド"""
        velocities = np.array(self.velocity_history)  # 速度履歴をNumPy配列に変換
        velocities = velocities.reshape(-1, 2)  # 位置データを (N, 2) の形に整形
        times = np.array(self.time_history)  # 時間履歴をNumPy配列に変換

        plt.figure(figsize=(10, 5))
        plt.plot(times, velocities[:, 0], label='X Velocity', color='blue')  # X速度
        # plt.plot(times, velocities[:, 1], label='Y Velocity', color='red')   # Y速度
        plt.title('Velocity of the Simulator Object')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid()
        plt.savefig(filename)  # 画像として保存
        plt.close()  # プロットを閉じる

# ソケット通信でデータを送信
def send_position_data(socket_client, position1, position2, velocity1, velocity2,time):
    """2つのオブジェクトの位置データをソケットを介して送信するメソッド"""
    message = f"{position1[0, 0]:.1f},{position1[0, 1]:.1f},{position2[0, 0]:.1f},{position2[0, 1]:.1f},{velocity1[0, 0]:.1f},{velocity1[0, 1]:.1f},{velocity2[0, 0]:.1f},{velocity2[0, 1]:.1f},{time:.1f}\n"
    socket_client.send(message.encode('utf-8'))

# メイン処理
# このコードでは2物体のシミュレーションを行うコトを目的としている
if __name__ == '__main__':
    # ソケット設定
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((host, port))
    
    # シミュレーションの初期値設定
    # 設定値はどんなことがあってもSI単位で記載のこと。また、100 g → 0.1 kg のように変更のこと
    object1_init_pos = [-500, 25] # (Px,Py) [m]
    object1_init_vel = [10, 0] # (Vx, Vy) [m/s]
    object2_init_pos = [-500.0, -25.0] # (Px,Py) [m]
    object2_init_vel = [5.0, 0.0] # (Vx, Vy) [m/s]
    object1_mass = 10
    object2_mass = 10
    external_force = [1,0]
    
    # シミュレーションオブジェクトの作成
    object1 = SimulatorObject(position=object1_init_pos, velocity=object1_init_vel)
    object2 = SimulatorObject(position=object2_init_pos, velocity=object2_init_vel)

    # パラメータを設定（時間変化する場合はシミュレーションループ内で設定すること
    object1.set_mass(object1_mass)
    object2.set_mass(object2_mass)
    
    # シミュレーションパラメータ
    h = 0.001  # タイムステップ(もう少し大きくしても良い)
    total_time = 50  # 総シミュレーション時間
    steps = int(total_time / h)

    # シミュレーションループ
    send_interval = 0.1  # データ送信の間隔（秒）
    next_send_time = 0.0  # 次に送信する時刻　
    for step in range(steps):
        # 時間更新
        t = step * h
        
        # 外力設定
        if(abs(object1.velocity[0,0] - object2.velocity[0,0])<=0.01):
            object1.set_force([0,0])
            object2.set_force([0,0])
            # break
        elif (object1.velocity[0,0] > object2.velocity[0,0]):
            object1.set_force(-np.array(external_force))
            object2.set_force(external_force)
        elif (object1.velocity[0,0] < object2.velocity[0,0]):
            object1.set_force(external_force)
            object2.set_force(-np.array(external_force))
        # else:
        #     object1.set_force([0,0])
        #     object2.set_force([0,0])
        
        # 物体の位置と速度を更新（4次のルンゲクッタ法）
        object1.rk4(h, t)
        object2.rk4(h, t)
        print(f"time: {t:.2f} sec")
        
        # 0.1秒ごとにデータ送信
        if t >= next_send_time:
            send_position_data(socket_client, object1.position, object2.position, object1.velocity, object2.velocity,t)
            next_send_time += send_interval  # 次の送信時刻を更新

    # ソケット通信を終了
    socket_client.close()
    # シミュレーション終了後に位置と速度をプロットして画像として保存
    object1.plot_trajectory("object1_trajectory.png")  # Object 1の位置を保存
    object1.plot_velocity("object1_velocity.png")      # Object 1の速度を保存
    object2.plot_trajectory("object2_trajectory.png")  # Object 2の位置を保存
    object2.plot_velocity("object2_velocity.png")      # Object 2の速度を保存
