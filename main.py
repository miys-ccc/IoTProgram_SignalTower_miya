# IoT_Program.py 光センサー

import serial
from datetime import datetime
from time import sleep


# -------------------------------------------------------------------------------
# InfluxDB
# -------------------------------------------------------------------------------

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDBサーバーのIPアドレスとポート
url = "http://localhost:8086"                # URL
org = "IoT Development"                      # 対象organization
bucket = "SignalTower"                       # 対象bucket
token = "siLd0Z4TAl8TboKQiIEijtKfHODXK" \
        "amBXBvNkYJV3GuPvMcV8yTFYQruWY" \
        "2HsApryAyf61LmpCPgfNVoJWmAtg=="     # 発行したToken

client = InfluxDBClient(
    url=url,
    token=token,
    org=org,
    database='SignalTowerDB',
)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


# -----------------------------------------------------------------------------------------
# 時刻取り出し
# -----------------------------------------------------------------------------------------
def getNow():
    now = datetime.now()
    date = "{:%Y-%m-%d %H}".format(now)
    hour = now.hour
    mini = now.min
    return now, date, hour, mini


# -----------------------------------------------------------------------------------------
# データ読み込み関数 (論理デバイスID,センサ情報)
# -----------------------------------------------------------------------------------------
def readSerial(ser, now):
    line = ser.readline().rstrip()
    line = line.strip().decode('utf-8')
    list2 = [line[i:i+2] for i in range(1, len(line), 2)]

    if len(list2) != 24:
        return '-1', 0, 0.0, 0, 0             # 異常データでリターン

    list = []
    for i in range(0, len(list2), 1):
        n = int(list2[i], 16)
        list.append(n)                        # listに追加
    list.pop()                                # チェックサムを削除

    lid = list[0]                             # 論理デバイスID
    ladr = list[5] << 24 | list[6] << 16 | list[7] << 8 | list[8]        # 個別識別番号

    ad = {}                                                              # アナログデータ

    for i in range(1,5):                            # AD値1〜4 の復元
        av = list[i + 18 - 1]                       # [18] 〜 [21]
        if (av == 0xFF):
            ad[i] = -1
        else:
            ad[i] = av

    id = "{:02X}".format(ladr)                     # 個別識別番号
    lampValue = int(ad[1])                         # センサ情報

    return lid, id, lampValue


# -----------------------------------------------------------------------------------------
# メイン関数
# -----------------------------------------------------------------------------------------
def main():
    print("--- dateAquisition start ---")

    ser = serial.Serial("/dev/tty.usbserial-MW7H3JEX", 115200)  # Serialのインスタンス化

    try:
        while True:
            now, date, hour, mini = getNow()                                # 現在時刻の取り出し
            lid, id, lampValue = readSerial(ser, now)                       # シリアルデータ読み出し

            if lampValue == -1:         # 異常検知
                lampON = 0
                lampOFF = 0
            elif lampValue < 45:
                lampON = 1              # 点灯
                lampOFF = 0             # 消灯
            else:
                lampON = 0              # 点灯
                lampOFF = 1             # 消灯

            print(
                "{:%Y/%m/%d %H:%M:%S}".format(now),
                "|",
                "sensor:", lampValue,
                "lampON:", lampON,
                "lampOFF:", lampOFF,
                end="\n"
            )

            # 現在の日時と曜日を取得します
            now = datetime.now()                                            # 現在の日時を取得
            weekdays = ["月", "火", "水", "木", "金", "土", "日"]              # 日本語の曜日のリストを定義
            date_format = f'{now.year}年{now.month}月{now.day}日({weekdays[now.weekday()]}) '\
                          f'{now.hour}時{now.minute}分'
            # print(date_format)

            sleep(1)                                                        # 1sスリープ

            # -----------------------------------------------------------------------------------------
            # データベースへ書き込み
            # -----------------------------------------------------------------------------------------
            data = (
                Point("SignalTower")                         # データベース名
                .tag("id", id)                               # 子機ID
                .field("lampON", lampON)                     # 点灯
                .field("lampOFF", lampOFF)                   # 消灯
                .field("date_format", date_format)           # 時刻
            )

            write_api.write(bucket=bucket, record=data)

            # -----------------------------------------------------------------------------------------
            # InfluxDBのバケット設定でデータ保存期間は、90日間
            # -----------------------------------------------------------------------------------------

    except KeyboardInterrupt:
        pass

    # print("lid:", lid, "id:", id, end="\n")
    print("--- dateAquisition end ---")

    ser.close()   # センサーのシリアル通信を停止


# -------------------------------------------------------------------------------
if __name__ == "__main__":   # プログラムの起点
    main()

