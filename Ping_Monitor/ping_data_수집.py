import subprocess
import re
import pymysql
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

sched = BlockingScheduler()

def create_database_and_table():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='enchem135!@',
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS enchem_scan CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        cursor.execute("USE enchem_scan")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ping_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                host_name VARCHAR(255),
                host_ip VARCHAR(255),
                ping_date DATETIME,
                status INT,
                ping_min INT,
                ping_max INT,
                ping_avg INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """)
        conn.commit()
        print("Database 'enchem_scan' and table 'ping_data' created successfully.")

    except Exception as e:
        print("Error creating database and table:", e)

def ping_and_insert_data(host_name, host_ip):
    p = re.compile(rb'[=]\s(\d+)[m][s]')

    cmd = f'ping -n 3 {host_ip}'
    try:
        output = subprocess.check_output(cmd, shell=True)

        pings = p.findall(output)

        # 바이트를 정수로 변환하여 최소, 최대, 평균을 계산합니다.
        pings = [int(ping.decode('utf-8')) for ping in pings]
        min_ping = min(pings)
        max_ping = max(pings)
        avg_ping = sum(pings) // len(pings)

        ping_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(host_name, host_ip, min_ping, max_ping, avg_ping)

        # MariaDB 접속정보
        maria_host = 'localhost'
        maria_port = 3306
        maria_user = 'root'
        maria_password = 'enchem135!@'
        maria_database = 'enchem_scan'

        # MariaDB Conn
        conn = pymysql.connect(
            host=maria_host,
            port=maria_port,
            user=maria_user,
            password=maria_password,
            database=maria_database
        )

        sql = "INSERT INTO ping_data (host_name, host_ip, ping_date, status, ping_min, ping_max, ping_avg) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (host_name, host_ip, ping_date, 0, min_ping, max_ping, avg_ping))
                conn.commit()

        print(f"Data inserted for {host_name} ({host_ip}) at {ping_date}")

    except subprocess.CalledProcessError:
        status = min_ping = max_ping = avg_ping = 999
        ping_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # MariaDB 접속정보
        maria_host = 'localhost'
        maria_port = 3306
        maria_user = 'root'
        maria_password = 'enchem135!@'
        maria_database = 'enchem_scan'

        # MariaDB Conn
        conn = pymysql.connect(
            host=maria_host,
            port=maria_port,
            user=maria_user,
            password=maria_password,
            database=maria_database
        )

        sql = "INSERT INTO ping_data (host_name, host_ip, ping_date, status, ping_min, ping_max, ping_avg) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (host_name,host_ip, ping_date, status, min_ping, max_ping, avg_ping))
                conn.commit()

        print(f"Failed to ping {host_name} ({host_ip}), Data inserted with default values at {ping_date}")

def process_hosts():
    path = "C:/Users/KiNyeon.Kim/Documents/Python/Enchem/Ping/list.txt"

    with open(path, 'r', encoding='UTF-8') as f:
        lines = f.readlines()

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 2:  # 두 개의 요소로 분리되는지 확인합니다.
                host_name = parts[0].strip()  # 장치 이름
                host_ip = parts[1].strip()  # IP 주소

                # 쓰레드를 생성하여 ping_and_insert_data 함수를 실행합니다.
                threading.Thread(target=ping_and_insert_data, args=(host_name, host_ip)).start()

if __name__ == "__main__":
    create_database_and_table()
    process_hosts()

@sched.scheduled_job('interval', seconds=60, id='run_1')
def Start():
    process_hosts()

sched.start()
