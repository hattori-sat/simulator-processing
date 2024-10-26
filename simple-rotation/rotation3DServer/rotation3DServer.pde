import processing.net.*;  // ネットワーク通信用のライブラリをインポート

// 変数の定義(server周りはpythonのコードに合わせます)
int port = 10001;  // サーバーが待機するポート番号
Server server;  // サーバーオブジェクトを定義
float angleX = 0.0;  // X軸周りの回転角度
float angleY = 0.0;  // Y軸周りの回転角度
PVector axisX;  // X軸のベクトル
PVector axisY;  // Y軸のベクトル
PVector axisZ;  // Z軸のベクトル

// 最初に一回呼ばれる関数。Arduinoとかと同じ
void setup() {
  size(800, 600, P3D);  // ウィンドウサイズと3D描画モードを設定
  server = new Server(this, port);  // サーバーを初期化し、指定ポートで待機
  println("server address: " + server.ip());  // サーバーのIPアドレスを表示
  axisX = new PVector(1,0,0);  // X軸の単位ベクトルを設定
  axisY = new PVector(0,1,0);  // Y軸の単位ベクトルを設定
  axisZ = new PVector(0,0,1);  // Z軸の単位ベクトルを設定
}

// 以下のコードが繰り返される
// pythonから送られてくるmessageは常に1が送られます
void draw() {
  background(255);  // 背景を白にリセット

  Client client = server.available();  // クライアントからの接続があるかチェック
  if (client != null) {  // クライアントが存在する場合
    String message = client.readString();  // クライアントから送られたメッセージを読み取る
    if (message != null && message.length() > 0) {  // メッセージが空でない場合
      // Pythonからの回転速度のデータを解析し、X軸とY軸の回転角度に加算
      float rotationSpeedX = float(message);  // 文字列を数値に変換（X軸用）
      float rotationSpeedY = float(message);  // 文字列を数値に変換（Y軸用）
      angleX += rotationSpeedX;  // X軸回転角度に加算
      angleY += rotationSpeedY;  // Y軸回転角度に加算
    }
  }

  // 3D物体（立方体）を描画
  translate(width / 2, height / 2, 0);  // 画面の中心に座標を移動
  rotateX(radians(angleX));  // X軸周りに回転
  rotateY(radians(angleY));  // Y軸周りに回転
  fill(0, 0, 255);  // 立方体の色を青に設定
  box(50);  // サイズ50の立方体を描画
}
