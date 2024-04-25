from datetime import datetime
from pysnmp.hlapi import *

# SNMP 커뮤니티 문자열
community = 'public'

# SNMP OID 정의
printer_usage_oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'  # 프린터 사용량 OID
yellow_ink_level_oid = '1.3.6.1.2.1.43.11.1.1.9.1.3'  # 노란색 잉크 잔량 OID
magenta_ink_level_oid = '1.3.6.1.2.1.43.11.1.1.9.1.2'  # 마젠타색 잉크 잔량 OID
cyan_ink_level_oid = '1.3.6.1.2.1.43.11.1.1.9.1.1'  # 시안색 잉크 잔량 OID
black_ink_level_oid = '1.3.6.1.2.1.43.11.1.1.9.1.4'  # 검정색 잉크 잔량 OID
print_counter_bw_oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'  # 흑백 프린터 횟수 OID
print_counter_color_oid = '1.3.6.1.2.1.43.10.2.1.5.1.1'  # 컬러 프린터 횟수 OID
print_Serial_Number_oid = '1.3.6.1.2.1.1.1.0'   # 제품 일련번호 OID
error_log_oid = '1.3.6.1.2.1.25.1.8.0'  # 프린터 에러 로그 OID
alter_log_oid = '1.3.6.1.2.1.43.11'

def get_snmp_data(ip_address, oid):
    start_time = datetime.now()
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip_address, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    end_time = datetime.now()

    if errorIndication:
        print(f"IP 주소 {ip_address}: SNMP 오류 - {errorIndication}")
        return None, None
    elif errorStatus:
        print(f"IP 주소 {ip_address}: SNMP 오류 - {errorStatus}")
        print(f"IP 주소 {ip_address}: SNMP 오류 인덱스 - {errorIndex}")
        return None, None
    else:
        return varBinds[0][1], end_time - start_time

# 프린터 정보 가져오기
ip_addresses = [
    '192.168.21.239',
    '192.168.21.199',
    '192.168.20.4',
    '192.168.20.211',
    '192.168.20.214',
    '192.168.20.213',
    '192.168.20.199',
    '192.168.21.240',
    '192.168.21.230',
    '192.168.21.250',
    '192.168.21.255',
    '172.30.1.99',
    '172.30.1.32',
    '192.168.10.100',
    '192.168.20.201',
    '192.168.21.242',
    '192.168.20.243'    
]


# ip_addresses = [
#     '192.168.20.201'
#     # '192.168.21.242',
#     # '192.168.20.243'
# ]

current_time = datetime.now()
print(f"현재 시간: {current_time}\n")

for ip_address in ip_addresses:
    printer_usage, query_time = get_snmp_data(ip_address, printer_usage_oid)
    yellow_ink_level, _ = get_snmp_data(ip_address, yellow_ink_level_oid)
    magenta_ink_level, _ = get_snmp_data(ip_address, magenta_ink_level_oid)
    cyan_ink_level, _ = get_snmp_data(ip_address, cyan_ink_level_oid)
    black_ink_level, _ = get_snmp_data(ip_address, black_ink_level_oid)
    print_counter_bw, _ = get_snmp_data(ip_address, print_counter_bw_oid)
    print_counter_color, _ = get_snmp_data(ip_address, print_counter_color_oid)
    print_Serial_Number, _ = get_snmp_data(ip_address, print_Serial_Number_oid)
    error_log, _ = get_snmp_data(ip_address, error_log_oid)
    alter_log, _ = get_snmp_data(ip_address, alter_log_oid)

    print_Serial_Number_str = str(print_Serial_Number)
    split_text = print_Serial_Number_str.split(";")
    model = split_text[0]
    serial_number = split_text[-1].split("S/N ")[-1]

    # 결과 출력
    print(f"IP 주소: {ip_address}")
    print(f"모델명 : {model}")
    print(f"제품일련번호 : {serial_number}")
    print(f"조회 시간: {datetime.now()}")
    print("프린터 사용량:", printer_usage)
    print("노란색 잉크 잔량:", yellow_ink_level)
    print("마젠타색 잉크 잔량:", magenta_ink_level)
    print("시안색 잉크 잔량:", cyan_ink_level)
    print("검정색 잉크 잔량:", black_ink_level)
    print("흑백 프린터 횟수:", print_counter_bw)
    print("컬러 프린터 횟수:", print_counter_color)
    print("에러 로그:", error_log)
    print("Alter Log :", alter_log)
    print("조회 시간:", query_time)
    print("-" * 50)
