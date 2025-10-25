from pydantic import BaseModel
import requests
import socket
import time
from pythonping import ping as pping
from typing import List, Union
from fastapi import FastAPI, Request, Response

app = FastAPI()

# Тип возвращаемого значения: 
# [bool (успех/неудача), float (время в мс) или list[str] (список IP-адресов)]
# Тип возвращаемого значения для Ping, HTTP и TCP-порта: [bool (успех/неудача), float (время в мс)]
TimeResult = List[Union[bool, float]]
# Тип возвращаемого значения для Traceroute: [bool (успех/неудача), list[str] (список IP-адресов)]
TraceResult = List[Union[bool, List[str]]]

# Максимальное количество переходов для трассировки
MAX_HOPS = 30
# Порт для TCP-трассировки (используем 80)
TRACE_PORT = 80 
# Таймаут для каждого прыжка в секундах
HOP_TIMEOUT = 1.0 

# 1. Проверка HTTP/HTTPS
def check_http_https(host: str) -> TimeResult:
    protocols = ['https://', 'http://']
    timeout = 5
    
    for proto in protocols:
        url = proto + host
        try:
            start_time = time.time()
            requests.head(url, timeout=timeout, allow_redirects=True)
            elapsed_time = (time.time() - start_time) * 1000 
            elapsed_time = round(elapsed_time)
            return [True, elapsed_time]
        except requests.exceptions.RequestException:
            continue
            
    # Если оба протокола не удались
    return [False, 0.0]

# 2. Проверка Ping (ICMP)
def check_ping(host: str) -> TimeResult:
    try:
        response_list = pping(host, count=3, timeout=2, verbose=False)
        
        if response_list.success:
            # pythonping возвращает время в мс
            return [True, response_list.rtt_avg_ms * 1000]
        else:
            return [False, 0.0]
    except Exception:
        # Если возникает исключение (например, неверный хост)
        return [False, 0.0]

# 3. Проверка TCP-порта
def check_tcp_port(host: str, port: int = 80) -> TimeResult:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        start_time = time.time()
        result = sock.connect_ex((host, port))
        # ПЕРЕВЕДЕНО В МИЛЛИСЕКУНДЫ
        elapsed_time = (time.time() - start_time) * 1000 
        sock.close()

        if result == 0:
            return [True, round(elapsed_time)]
        else:
            return [False, 0.0]

    except (socket.gaierror, Exception):
        # Если возникает исключение (например, неверный хост)
        return [False, 0.0]

# 4. Traceroute (Специализированная TCP-трассировка без прав администратора)
# NOTE: Для надежного возврата IP-адресов промежуточных узлов без прав 
# администратора требуется более сложный инструмент или вызов внешней утилиты.
# Я адаптирую ваш код к требуемому формату вывода, делая трассировку максимально 
# простой (и, соответственно, менее надежной, но не требующей root).

def check_traceroute(host: str) -> TraceResult:
    route_list = []
    
    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        return [False, ["Ошибка: Не удалось разрешить доменное имя."]]

    for ttl in range(1, MAX_HOPS + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(HOP_TIMEOUT)
        
        # Установка TTL для исходящего сокета
        if hasattr(socket, 'IP_TTL'):
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        # Успешно установить TTL без root часто невозможно, 
        # поэтому код может сработать только на Windows или с cap_net_raw.

        try:
            # Отправляем SYN-пакет на целевой порт
            sock.connect((dest_ip, TRACE_PORT))
            
            # Достигли цели (соединение установлено)
            route_list.append(dest_ip)
            sock.close()
            return [True, route_list]

        except socket.timeout:
            # Таймаут - невозможно получить адрес узла без root
            route_list.append('* * *')
        
        except socket.error as e:
            # Если возникла ошибка, мы предполагаем, что TTL истек и 
            # ОС перехватила ICMP Time Exceeded (очень ненадежно без root).
            
            # Мы не можем надежно получить IP узла без сырых сокетов.
            # Если код ошибки 10061 (Connection Refused), мы достигли цели.
            if e.errno == 10061: 
                route_list.append(dest_ip)
                return [True, route_list]
            
            route_list.append('* * *') # Все остальные ошибки или таймаут

        finally:
            if 'sock' in locals():
                 sock.close()
            
        if ttl == MAX_HOPS:
            # Достигнуто максимальное количество переходов без достижения цели
            return [False, route_list]
            
    return [False, ["Трассировка завершена неудачей."]]

#Api

class reportFromAgent(BaseModel):
    country: str
    UIID: str
    taskUIID: str
    result: str

class checkRequest(BaseModel):
    target: str
    task: str

@app.post("/check")
def check(validReq: checkRequest):
    match validReq.task:
        case "http(s)":
            return check_http_https(validReq.target)
        case "ping":
            return check_ping(validReq.target)

if __name__ == '__main__':
    HOST_TO_TEST = "apple.com"

    print(f"========================================\nТестирование хоста: {HOST_TO_TEST}\n========================================")

    # 1. HTTP/HTTPS
    http_result = check_http_https(HOST_TO_TEST)
    print(f"🌐 HTTP/HTTPS (bool, time_ms): {http_result}")

    # 2. Ping
    ping_result = check_ping(HOST_TO_TEST)
    print(f"🟢 Ping (bool, avg_time_ms): {ping_result}")

    # 3. TCP-порт (443)
    tcp_443_result = check_tcp_port(HOST_TO_TEST, port=443)
    print(f"🚪 TCP-порт 443 (bool, time_ms): {tcp_443_result}")

    # 4. Traceroute (TCP-трассировка без админа)
    trace_result = check_traceroute(HOST_TO_TEST)
    print(f"\n--- 🛣️ Traceroute (bool, IP_List) ---")
    print(f"Успех: {trace_result}")
