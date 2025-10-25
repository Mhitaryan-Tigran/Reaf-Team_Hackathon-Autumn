from pydantic import BaseModel
import requests
import socket
import time
from pythonping import ping as pping
from typing import List, Union
from fastapi import FastAPI
from scapy.all import IP, ICMP, sr1
from scapy.layers.inet import UDP

app = FastAPI()

# Типы результатов
TimeResult = List[Union[bool, float]]
TraceResult = List[Union[bool, List[str]]]

MAX_HOPS = 30
TRACE_PORT = 80
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
            return [True, round(elapsed_time)]
        except requests.exceptions.RequestException:
            continue
            
    return [False, 0.0]

# 2. Проверка Ping (ICMP)
def check_ping(host: str) -> TimeResult:
    try:
        response_list = pping(host, count=3, timeout=2, verbose=False)
        if response_list.success():
            return [True, round(response_list.rtt_avg_ms)]
        else:
            return [False, 0.0]
    except Exception:
        return [False, 0.0]

# 3. Проверка TCP-порта
def check_tcp_port(host: str) -> TimeResult:
    addr = host.split(":")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        start_time = time.time()
        result = sock.connect_ex((addr[0], int(addr[1])))
        elapsed_time = (time.time() - start_time) * 1000
        sock.close()
        if result == 0:
            return [True, round(elapsed_time)]
        else:
            return [False, 0.0]
    except Exception:
        return [False, 0.0]

# 4. Низкоуровневая трассировка (manual_traceroute)
def manual_traceroute(destination: str, max_hops: int = 30) -> List[str]:
    reply_list = []
    try:
        destination_ip = socket.gethostbyname(destination)
    except socket.gaierror:
        return 

    for ttl in range(1, max_hops + 1):
        packet = IP(dst=destination_ip, ttl=ttl) / UDP(dport=33434)
        reply = sr1(packet, verbose=0, timeout=2)
        if reply is None:
            continue
        reply_list.append(reply.src)
        if reply.type == 3:  # Reached destination
            break
    return reply_list

# 5. Обертка для API: check_traceroute
def check_traceroute(host: str) -> TraceResult:
    try:
        hops = manual_traceroute(host, MAX_HOPS)
        if hops:
            return [True, hops]
        else:
            return [False, []]
    except Exception:
        return [False, []]

# === Модели запросов ===

class reportFromAgent(BaseModel):
    country: str
    UIID: str
    taskUIID: str
    result: str

class checkRequest(BaseModel):
    target: str
    task: str

# === Основное API ===

@app.post("/check")
def check(validReq: checkRequest):
    match validReq.task:
        case "http(s)":
            return check_http_https(validReq.target)
        case "ping":
            return check_ping(validReq.target)
        case "tcp":
            return check_tcp_port(validReq.target)
        case "traceroute":
            return check_traceroute(validReq.target)
        case _:
            return {"error": "Unknown task"}

# === Локальное тестирование ===

if __name__ == '__main__':
    HOST_TO_TEST = "google.com"

    print(f"========================================\nТестирование хоста: {HOST_TO_TEST}\n========================================")

    # 1. HTTP/HTTPS
    print(f"🌐 HTTP/HTTPS: {check_http_https(HOST_TO_TEST)}")

    # 2. Ping
    print(f"🟢 Ping: {check_ping(HOST_TO_TEST)}")

    # 3. TCP-порт (443)
    print(f"🚪 TCP 443: {check_tcp_port(f'{HOST_TO_TEST}:443')}")

    # 4. Traceroute
    print(f"🛣️ Traceroute: {check_traceroute(HOST_TO_TEST)}")
