sudo apt update
sudo apt install -y build-essential zlib1g-dev

wget https://golang.org/dl/go1.16.5.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.16.5.linux-armv6l.tar.gz
export PATH=$PATH:/usr/local/go/bin


git clone https://github.com/influxdata/influxdb.git
cd influxdb

make

./bin/influxd
