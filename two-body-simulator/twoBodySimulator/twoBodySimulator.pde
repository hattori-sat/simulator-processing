import processing.net.*;  // ネットワーク通信のためのライブラリをインポート
import processing.core.PVector;  // 2Dベクトル計算を行うためのPVectorクラスをインポート

// 変数定義
// pythonで設定した通信の設定に合わせる
int port = 10001;  // サーバーが待機するポート番号
Server server;  // サーバーオブジェクトを定義（クライアントからの接続を受け取るため）
PVector position1 = new PVector(0, 0);  // 1つ目の物体の位置を管理するベクトル
PVector position2 = new PVector(0, 0);  // 2つ目の物体の位置を管理するベクトル
PVector velocity1 = new PVector(0, 0);  // 1つ目の物体の位置を管理するベクトル
PVector velocity2 = new PVector(0, 0);  // 2つ目の物体の位置を管理するベクトル
int basic_vector_len = 30;  // 座標軸の基底ベクトルの長さ
PVector basic_vec_x = new PVector(basic_vector_len, 0);  // X軸方向の基底ベクトル
PVector basic_vec_y = new PVector(0, basic_vector_len);  // Y軸方向の基底ベクトル
float time = 0;

// 最初に一回だけ呼ばれる関数
void setup() {
  size(1400, 960);  // ウィンドウサイズを1000x1000ピクセルに設定
  server = new Server(this, port);  // サーバーを初期化し、指定ポートで接続待機
  println("server address: " + server.ip());  // サーバーのIPアドレスをコンソールに表示
}

// このdraw()がループして実行される
// pushMatrixとpopMatrixの概念が難しいと思うのでzennで説明します。
void draw() {
  background(255);  // 背景色を白にリセット（毎フレーム描画を更新）

  // ウィンドウの中心に座標を移動し、基準軸を描画
  pushMatrix();  // 現在の座標系を保存
  translate(width / 2, height / 2);  // 中心に座標を移動
//   drawAxes();  // 中心位置に座標軸を描画
  popMatrix();  // 座標系を元に戻す

  // クライアントからのメッセージをチェック
  Client client = server.available();  // 新しいクライアント接続があるか確認
  if (client != null) {  // クライアントが存在する場合
    String message = client.readString();  // クライアントからのメッセージを読み取る
    if (message != null && message.length() > 0) {  // メッセージが空でない場合のみ処理
      String[] data = split(message, ',');  // メッセージをカンマで分割し、各位置を取得
      if (data.length == 9) {  // データの長さが4（x1, y1, x2, y2）であることを確認
        position1.set(float(data[0]), -float(data[1]));  // 1つ目の物体の位置を設定
        position2.set(float(data[2]), -float(data[3]));  // 2つ目の物体の位置を設定
        velocity1.set(float(data[4]), float(data[5]));  // 1つ目の物体の位置を設定
        velocity2.set(float(data[6]), float(data[7]));  // 2つ目の物体の位置を設定
        time = float(data[8]);
      }
    }
  }

  // 1つ目の物体（青い四角形）を描画
  pushMatrix();  // 現在の座標系を保存
  translate(width / 2 + position1.x, height / 2 + position1.y);  // 指定位置に移動
  fill(0, 0, 255);  // 四角形を青色に設定
  rectMode(CENTER);  // 四角形の中心を基準点として描画
  rect(0, 0, 200, 50);  // 幅30、高さ30の四角形を描画
//   drawAxes();  // 四角形の位置に小さな座標軸を描画
  popMatrix();  // 座標系を元に戻す

  // 2つ目の物体（赤い四角形）を描画
  pushMatrix();  // 現在の座標系を保存
  translate(width / 2 + position2.x, height / 2 + position2.y);  // 指定位置に移動
  fill(255, 0, 0);  // 四角形を赤色に設定
  rectMode(CENTER);  // 四角形の中心を基準点として描画
  rect(0, 0, 200, 50);  // 四角形を描画
//   drawAxes();  // 四角形の位置に小さな座標軸を描画
  popMatrix();  // 座標系を元に戻す
  // 位置と速度を左上に表示
  fill(0);  // テキストの色を黒に設定
  textSize(20);  // テキストサイズを設定
  text("time : "+time,10,30);
  text("Object 1 data (Bule)",10, 60);
  text("Object 1 Position: (" + position1.x + ", " + -position1.y + ")", 10, 80);
  text("Object 1 Velocity: (" + velocity1.x + ", " + velocity1.y + ")", 10, 100);
  text("Object 2 data (Red)",10,130);
  text("Object 2 Position: (" + position2.x + ", " + -position2.y + ")", 10, 150);
  text("Object 2 Velocity: (" + velocity2.x + ", " + velocity2.y + ")", 10, 170);
}
