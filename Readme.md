# LiDAR Smoke Judge

LiDARでの霧検出用のスクリプト

scripts/LidarSmokeJudge.py に `LidarSmokeJudge`とテストコードを記載。
- is_in_smoke: 霧の中にいるか判定する
- smoke_filter: 霧の可能性がある点群にフラグを立てる

# Usage

## pacpデータを変換
pcapデータをダウンロード。

veloparserで任意のデータをtxtファイル化。
※ pcapから直接読み込みは未実装。今後実装したい。

```
$ git clone https://github.com/ArashJavan/veloparser.git
```

```
$ cd veloparser
$ python main.py -p {smoke.pcap} -o {out_data} -c params.yaml
```

## LiDARSmokeJudgeの実行

plot_LiDARSmokeJudge.py の下記を任意のディレクトリ、フレーム数として実行

```python
if __name__ == "__main__":
    # データが保存されているディレクトリのパス
    data_dir = '../data/smoke/velodynevlp16/data_ascii'
    start_frame = 180
    end_frame = 250
    visualizer = LiDARVisualizer(data_dir, start_frame, end_frame)
    visualizer.visualize_frames()
```

```
$ python .\plot_LiDARSmokeJudge.py
```
以下のようなグラフが出力されるはず。
![Alt text](image/image.png)