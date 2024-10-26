import processing.net.*;  // ネットワーク通信のためのライブラリをインポート
import processing.core.PVector;  // 2Dベクトル計算を行うためのPVectorクラスをインポート

// 変数定義
// pythonで設定した通信の設定に合わせる
int port = 10001;  // サーバーが待機するポート番号
Server server;  // サーバーオブジェクトを定義（クライアントからの接続を受け取るため）
PVector position1 = new PVector(0, 0);  // 1つ目の物体の位置を管理するベクトル
PVector position2 = new PVector(0, 0);  // 2つ目の物体の位置を管理するベクトル
int basic_vector_len = 30;  // 座標軸の基底ベクトルの長さ
PVector basic_vec_x = new PVector(basic_vector_len, 0);  // X軸方向の基底ベクトル
PVector basic_vec_y = new PVector(0, basic_vector_len);  // Y軸方向の基底ベクトル

// 最初に一回だけ呼ばれる関数
void setup() {
  size(1000, 1000);  // ウィンドウサイズを1000x1000ピクセルに設定
  server = new Server(this, port);  // サーバーを初期化し、指定ポートで接続待機
  println("server address: " + server.ip());  // サーバーのIPアドレスをコンソールに表示
}

// このdraw()がループして実行される
// pushMatrixとpopMatrixの概念が難しいと思うのでzennで説明します。
void draw() {
  background(0);  // 背景色を黒にリセット（毎フレーム描画を更新）

  // ウィンドウの中心に座標を移動し、基準軸を描画
  pushMatrix();  // 現在の座標系を保存
  translate(width / 2, height / 2);  // 中心に座標を移動
  drawAxes();  // 中心位置に座標軸を描画
  popMatrix();  // 座標系を元に戻す

  // クライアントからのメッセージをチェック
  Client client = server.available();  // 新しいクライアント接続があるか確認
  if (client != null) {  // クライアントが存在する場合
    String message = client.readString();  // クライアントからのメッセージを読み取る
    if (message != null && message.length() > 0) {  // メッセージが空でない場合のみ処理
      String[] data = split(message, ',');  // メッセージをカンマで分割し、各位置を取得
      if (data.length == 4) {  // データの長さが4（x1, y1, x2, y2）であることを確認
        position1.set(float(data[0]), float(data[1]));  // 1つ目の物体の位置を設定
        position2.set(float(data[2]), float(data[3]));  // 2つ目の物体の位置を設定
      }
    }
  }

  // 1つ目の物体（青い四角形）を描画
  pushMatrix();  // 現在の座標系を保存
  translate(width / 2 + position1.x, height / 2 + position1.y);  // 指定位置に移動
  fill(0, 0, 255);  // 四角形を青色に設定
  rectMode(CENTER);  // 四角形の中心を基準点として描画
  rect(0, 0, 30, 30);  // 幅30、高さ30の四角形を描画
  drawAxes();  // 四角形の位置に小さな座標軸を描画
  popMatrix();  // 座標系を元に戻す

  // 2つ目の物体（赤い四角形）を描画
  pushMatrix();  // 現在の座標系を保存
  translate(width / 2 + position2.x, height / 2 + position2.y);  // 指定位置に移動
  fill(255, 0, 0);  // 四角形を赤色に設定
  rectMode(CENTER);  // 四角形の中心を基準点として描画
  rect(0, 0, 30, 30);  // 幅30、高さ30の四角形を描画
  drawAxes();  // 四角形の位置に小さな座標軸を描画
  popMatrix();  // 座標系を元に戻す
}

// 基本の座標軸（X軸とY軸）を描画する関数
void drawAxes() {
  drawAxis(basic_vec_x, color(255, 0, 0));  // X軸（赤色）を描画
  drawAxis(basic_vec_y, color(0, 255, 0));  // Y軸（緑色）を描画
}

// 1本の軸線を描画する関数
void drawAxis(PVector direction, int axisColor) {
  stroke(axisColor);  // 線の色を設定
  strokeWeight(3);  // 線の太さを設定
  line(0, 0, direction.x, direction.y);  // 原点から方向ベクトルに沿って線を引く
}
