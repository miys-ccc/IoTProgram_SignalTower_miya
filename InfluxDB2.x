1. InfluxDBの最新バージョンを「公式ぺーじに記載のコマンド」でインストール
2. 「公式ページに記載のコマンド」でファイルを解凍
3. 解凍したInfluxdbのファイルをコマンドで開く (cd ファイルパス)


wget https://github.com/influxdata/influxdb/releases/download/v2.7.1/influxdb2-2.7.1_linux_arm64.tar.gz

tar xvfz influxdb2-2.7.1_linux_arm64.tar.gz

cd influxdb2-2.7.1_linux_arm64

./influxd


■Grafana

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt update

sudo apt install -y grafana

sudo systemctl start grafana-server

sudo systemctl enable grafana-server

http://localhost:3000/
