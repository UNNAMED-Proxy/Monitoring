import tkinter as tk
import calendar
import pymssql
from datetime import datetime
import threading
import time

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("달력")
        self.root.geometry("1400x800")

        self.now = datetime.now()
        self.month_name = calendar.month_name[self.now.month]

        self.month = tk.StringVar()
        self.month.set(self.month_name)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.create_calendar()

        # 백그라운드에서 데이터 업데이트를 위한 스레드 시작
        self.update_thread = threading.Thread(target=self.update_data_thread)
        self.update_thread.daemon = True  # 메인 스레드가 종료되면 자동으로 종료되도록 설정
        self.update_thread.start()

    def create_calendar(self):
        self.clear_frame()
        month_label = tk.Label(self.calendar_frame, textvariable=self.month, font=("Arial", 14))
        month_label.grid(row=0, column=0, columnspan=7)

        week_days = ["일", "월", "화", "수", "목", "금", "토"]
        for i, day in enumerate(week_days):
            day_label = tk.Label(self.calendar_frame, text=day, width=30, height=5, font=("Arial", 12))
            day_label.grid(row=1, column=i)

        cal = calendar.monthcalendar(self.now.year, self.now.month)
        
        for i, week in enumerate(cal, start=1):
            # 일자
            for j, day in enumerate(week):
                day_frame = tk.Frame(self.calendar_frame, width=200, height=30, bg="gray", borderwidth=1)
                day_frame.grid(row=i*2, column=j, padx=5, pady=5)
                
                if day != 0:
                    cal_day = str(day) + " 일"
                    day_label = tk.Label(day_frame, text=cal_day, font=("Arial", 8), anchor="nw", justify="left", wraplength=150)
                    day_label.pack()

            # 일자 상세
            for j, day in enumerate(week):
                day_frame = tk.Frame(self.calendar_frame, width=200, height=100, bg="gray", borderwidth=1)
                day_frame.grid(row=i*2+1, column=j, padx=5, pady=5)
                
                if day != 0:
                    data = self.get_data(int(f"{self.now.year}{self.now.month:02d}"), day)
                    data_str = "\n".join(data) if data else str(day) + " 일"
                    day_label = tk.Label(day_frame, text=data_str, font=("Arial", 8), anchor="nw", justify="left", wraplength=150)
                    day_label.pack()

    def clear_frame(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

    def get_data(self, year_month, day):
        # MSSQL 연결
        conn = pymssql.connect(server=Ip, port=Port, user=User, password=PassWord, database=DataBase)
        cursor = conn.cursor()

        # SQL 쿼리 실행
        query = """
        SELECT B.EmpName, D.OrdName
        FROM _THRAdmOrdEmp AS A
        LEFT OUTER JOIN _TDAEmp AS B ON A.CompanySeq = B.CompanySeq AND A.EmpSeq = B.EmpSeq
        LEFT JOIN _THRAdmOrd AS D ON D.CompanySeq = A.CompanySeq AND D.OrdSeq = A.OrdSeq
        WHERE LEFT(A.OrdDate, 8) = %s
        """
        cursor.execute(query, (str(year_month) + str(str(day).zfill(2)),))

        # 결과 가져오기
        data = []
        for idx, row in enumerate(cursor.fetchall(), start=1):
            row_data = [str(cell) if cell is not None else "" for cell in row]
            data.append(f"{idx}. {row_data[0]}, {row_data[1]}")

        # 연결 닫기
        cursor.close()
        conn.close()

        return data if data else [" "]

    def update_data_thread(self):
        while True:
            # 10분마다 데이터를 업데이트
            time.sleep(60)
            self.root.after(0, self.create_calendar)  # 메인 스레드에 업데이트 요청을 보냄

root = tk.Tk()
app = CalendarApp(root)
root.mainloop()