# simulator-processing
物理シミュレータを簡単に行えるprocessingについての説明用のリポジトリです。  
まだ公開していませんが、processingに関する内容を記事に纏める予定です。


# simple-rotation
[simlae-rotation](/simple-rotation/)は最初に読むべきコード群です。
pythonとprocessingのコードの２つがあります。  
簡単なsocket通信を使っていますが、今回はあまり気にせずに**pythonがデータを送信**して、**processingがデータを受けて3Dの立方体を動かす**と思っていただければokです。

分けている理由としては、以下の2点があります。
- pythonで何らかの演算、processingは表示するだけと役割を分けたい
- pythonの方が物理シミュレーションを行える機能が多数ある。
