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

sudo cp bin/grafana-server /usr/local/bin/

sudo cp conf/defaults.ini /etc/grafana/

sudo mkdir -p /var/lib/grafana

sudo apt install -y libfontconfig1

sudo nano /etc/systemd/system/grafana.service

[Unit]
Description=Grafana
Wants=network-online.target
After=network-online.target

[Service]
User=pi
Group=pi
Type=simple
WorkingDirectory=/usr/local/bin
ExecStart=/usr/local/bin/grafana-server --config=/etc/grafana/defaults.ini --homepath=/usr/local/share/grafana --packaging=deb
Restart=always

[Install]
WantedBy=multi-user.target

sudo systemctl enable grafana.service
sudo systemctl start grafana.service


http://localhost:3000/

