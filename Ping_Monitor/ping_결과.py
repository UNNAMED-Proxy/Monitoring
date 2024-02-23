import tkinter as tk
import pymysql
import threading
import time

def read_host_info(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        host_info = [line.strip().split(',') for line in lines]
    return host_info

def get_host_status(host_ip):
    host_ip = host_ip.strip()

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='enchem135!@',  # 암호 설정
                                     database='enchem_scan',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT status FROM ping_data WHERE host_ip = '{host_ip}' ORDER BY ping_date DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                return result['status']
            else:
                return None
    except Exception as e:
        print("Error fetching host status:", e)
    finally:
        connection.close()

def update_host_status():
    while True:
        for card in canvas.find_all():
            canvas.delete(card)  # 이전에 그려진 모든 카드 삭제

        host_info = read_host_info("C:/Users/KiNyeon.Kim/Documents/Python/Enchem/Ping/list.txt")

        for i, (host_name, host_ip) in enumerate(host_info, start=1):
            row = (i - 1) // 5
            col = (i - 1) % 5

            x1 = col * (card_width + gap)
            y1 = row * (card_height + gap)
            x2 = x1 + card_width
            y2 = y1 + card_height

            host_status = get_host_status(host_ip)
            if host_status == 0:
                card_color = 'green'
            else:
                card_color = 'red'

            card = canvas.create_rectangle(x1, y1, x2, y2, fill=card_color)

            text_x = (x1 + x2) // 2
            text_y = (y1 + y2) // 2
            canvas.create_text(text_x, text_y, text=host_name, fill='white', font=('Helvetica', 10, 'bold'))

            canvas.create_text(text_x, text_y + 20, text=host_ip, fill='white')

        time.sleep(10)  # 10초 간격으로 호스트 정보 업데이트

def main():
    root = tk.Tk()
    root.title("Host Information")

    global canvas
    canvas = tk.Canvas(root, bg='white', width=1000, height=450)
    canvas.pack(fill=tk.BOTH, expand=True)

    global card_width, card_height, gap
    card_width = 180
    card_height = 60
    gap = 10

    threading.Thread(target=update_host_status, daemon=True).start()  # 호스트 정보 업데이트 스레드 시작

    root.mainloop()

if __name__ == "__main__":
    main()
