1. InfluxDBの最新バージョンを「公式ぺーじに記載のコマンド」でインストール
2. 「公式ページに記載のコマンド」でファイルを解凍
3. 解凍したInfluxdbのファイルをコマンドで開く (cd ファイルパス)


wget https://github.com/influxdata/influxdb/releases/download/v2.7.1/influxdb2-2.7.1_linux_arm64.tar.gz

tar xvfz influxdb2-2.7.1_linux_arm64.tar.gz

cd influxdb2-2.7.1_linux_arm64

./influxd


■Grafana

https://grafana.com/grafana/download?platform=linux



展開
tar -zxvf grafana-x.x.x.linux-armv7.tar.gz

cd grafana-x.x.x

./bin/grafana-server

http://localhost:3000/

