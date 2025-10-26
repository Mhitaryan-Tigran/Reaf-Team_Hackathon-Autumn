from pydantic import BaseModel
import requests
import socket
import time
import threading
import uuid
import os
import json
from pythonping import ping as pping
from typing import List, Union
from fastapi import FastAPI
from scapy.all import IP, ICMP, sr1
from scapy.layers.inet import UDP
from dotenv import load_dotenv
import dns.resolver
import subprocess
import re
import platform
from typing import Union
load_dotenv()


app = FastAPI()

agentUUID = os.getenv("agentUUID")
agentcountry = os.getenv("country")
masterIPandPort = os.getenv("masterIPandPort")

newTasks = []
completedTasks = []

backTHRWork = True

MAX_HOPS = 30
TRACE_PORT = 80
HOP_TIMEOUT = 1.0

def backgroundSender():
    global backTHRWork
    global completedTasks
    while backTHRWork:
        if completedTasks != []:
            print(completedTasks[0])
            body = {
                "country": str(agentcountry),
                "UIID": str(agentUUID),
                "taskUIID": str(completedTasks[0]['taskUUID']),
                "result": str(completedTasks[0]['result'])
            }
            req = requests.post(url=f"{masterIPandPort}/takeReport", data=json.dumps(body))

            completedTasks.pop(0)
        else:
            time.sleep(1)

def backgroundTasker():
    global newTasks
    global completedTasks
    global backTHRWork
    while backTHRWork:
        if newTasks != []:
            print(newTasks)
            match newTasks[0]["task"]:
                case "http(s)":
                    taskTocomplete = newTasks[0]
                    taskTocomplete["result"] = check_http_https(newTasks[0]["target"])
                    completedTasks.append(taskTocomplete)
                case "ping":
                    taskTocomplete = newTasks[0]
                    taskTocomplete["result"] = check_ping(newTasks[0]["target"])
                    completedTasks.append(taskTocomplete)
                case "tcp":
                    taskTocomplete = newTasks[0]
                    taskTocomplete["result"] = check_tcp_port(newTasks[0]["target"])
                    completedTasks.append(taskTocomplete)
                case "traceroute":
                    taskTocomplete = newTasks[0]
                    taskTocomplete["result"] = manual_traceroute(newTasks[0]["target"])
                    completedTasks.append(taskTocomplete)
                case "dns":
                    taskTocomplete = newTasks[0]
                    taskTocomplete["result"] = check_dns(newTasks[0]["target"])
                    completedTasks.append(taskTocomplete)
                case _:
                    return {"error": "Unknown task"}
            newTasks.pop(0)
        else:
            time.sleep(1)

@app.on_event("startup")
async def startDBConnection():
    threading.Thread(target=backgroundTasker).start()
    threading.Thread(target=backgroundSender).start()
    pass

@app.on_event("shutdown")
async def stopDBConnection():
    global backTHRWork
    backTHRWork = False

# 1. Проверка HTTP/HTTPS
def check_http_https(host: str):
    protocols = ['https://', 'http://']
    timeout = 5
    
    for proto in protocols:
        url = proto + host
        try:
            start_time = time.time()
            requests.head(url, timeout=timeout, allow_redirects=True)
            elapsed_time = (time.time() - start_time) * 1000
            return round(elapsed_time)
        except requests.exceptions.RequestException:
            continue
            
    return False

# 2. Ping
def check_ping(host: str) -> Union[int, bool]:
    system = platform.system()
    if system == "Windows":
        ping_param = "-n"
    else:
        ping_param = "-c"

    try:
        result = subprocess.run(
            ["ping", ping_param, "3", "-W", "2", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return False

        output = result.stdout

        
        if system == "Darwin":
            match = re.search(r"round-trip min/avg/max/stddev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms", output)
        else:  
            match = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms", output)

        if match:
            avg_rtt = float(match.group(1))
            return round(avg_rtt)
        else:
            return False

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False
    
# 3. TCP-порт
def check_tcp_port(host: str):
    addr = host.split(":")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        start_time = time.time()
        result = sock.connect_ex((addr[0], int(addr[1])))
        elapsed_time = (time.time() - start_time) * 1000
        sock.close()
        if result == 0:
            return round(elapsed_time)
        else:
            return False
    except Exception:
        return False

# 4. traceroute
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
        if reply.type == 3:
            break
    return reply_list

# 5. DNS lookup
def check_dns(host_and_type: str):
    """
    Формат: 'domain.com:A' или 'domain.com:MX' и т.д.
    Поддерживаемые типы: A, AAAA, MX, NS, TXT
    """
    try:
        parts = host_and_type.split(":")
        domain = parts[0]
        record_type = parts[1].upper() if len(parts) > 1 else "A"
        
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
        resolver.timeout = 3
        resolver.lifetime = 3
        
        start_time = time.time()
        answers = resolver.resolve(domain, record_type)
        elapsed_time = (time.time() - start_time) * 1000
        
        results = []
        for rdata in answers:
            if record_type == "MX":
                results.append(f"{rdata.preference} {rdata.exchange}")
            elif record_type == "TXT":
                results.append(str(rdata).strip('"'))
            else:
                results.append(str(rdata))
        
        return {
            "records": results,
            "time_ms": round(elapsed_time)
        }
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return False
    except Exception:
        return False

class reportFromAgent(BaseModel):
    country: str
    UIID: str
    taskUIID: str
    result: str

class checkRequest(BaseModel):
    target: str
    task: str
    taskUUID: str

# === Основное API ===

@app.post("/check")
def check(validReq: checkRequest):
    newTask = {
        "target": validReq.target,
        "task": validReq.task,
        "taskUUID": validReq.taskUUID
    }
    newTasks.append(newTask)

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
    print(f"🛣️ Traceroute: {manual_traceroute(HOST_TO_TEST)}")
    
    # 5. DNS lookup
    print(f"🔍 DNS A: {check_dns(f'{HOST_TO_TEST}:A')}")
    print(f"🔍 DNS AAAA: {check_dns(f'{HOST_TO_TEST}:AAAA')}")
    print(f"🔍 DNS MX: {check_dns(f'{HOST_TO_TEST}:MX')}")
    print(f"🔍 DNS NS: {check_dns(f'{HOST_TO_TEST}:NS')}")
    print(f"🔍 DNS TXT: {check_dns(f'{HOST_TO_TEST}:TXT')}")
