서버 모니터링

세로 list.txt 의 양에 맞게 가로 5개의 카드 고정으로 세로 카드 생성

1) MariaDB 에 Data Insert
 - (1). DataBase 유무 Check
   > 없을 경우 DataBase 생성 (명칭 : enchem_scan)

 - (2). Table 유무 Check
    > 없을 경우 Table 생성 (명칭 : ping_data)

2) Ping 은 멀티쓰레드로 ping 처리

3) ping 주기 : 60s

4) 화면출력 프로그램 DB Select 주기 : 10s
