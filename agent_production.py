"""
Host Checker Agent - Production Ready
Поддерживает: HTTP(S), Ping, TCP, Traceroute, DNS Lookup
"""

from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
import threading
import json
import time
import subprocess
import requests
import socket
import sys
import os
import dns.resolver
import dns.reversename
from typing import Dict, Any

# ============= CONFIGURATION =============

# Main server URL (where to send results)
MAIN_SERVER_URL = os.getenv("MAIN_SERVER_URL", "http://localhost:8000")

# Agent identification
AGENT_COUNTRY = os.getenv("AGENT_COUNTRY", "Russia")
AGENT_NAME = os.getenv("AGENT_NAME", "Agent-Moscow")
AGENT_UIID = os.getenv("AGENT_UIID", "")  # Will be set after registration
AGENT_API_TOKEN = os.getenv("AGENT_API_TOKEN", "")

# Polling configuration
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))  # seconds
MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "10"))

# ============= FASTAPI APP =============

app = FastAPI()

# Stopper for background threads
stopper = threading.Event()

# Task counter for concurrency control
active_tasks = 0
task_lock = threading.Lock()

# ============= MODELS =============

class CheckRequest(BaseModel):
    taskUIID: str
    check_type: str
    target: str

# ============= DNS LOOKUP FUNCTIONS =============

def run_dns_lookup(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """
    Выполняет DNS lookup
    Поддерживаемые типы: A, AAAA, MX, NS, TXT, CNAME
    """
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8', '1.1.1.1']  # Google DNS и Cloudflare
        resolver.timeout = 5
        resolver.lifetime = 5
        
        start_time = time.time()
        answers = resolver.resolve(domain, record_type)
        end_time = time.time()
        
        records = []
        for rdata in answers:
            if record_type == "MX":
                records.append({
                    "priority": rdata.preference,
                    "exchange": str(rdata.exchange)
                })
            elif record_type == "TXT":
                records.append({
                    "text": str(rdata)
                })
            elif record_type == "NS":
                records.append({
                    "nameserver": str(rdata)
                })
            else:
                records.append({
                    "address": str(rdata)
                })
        
        return {
            "success": True,
            "record_type": record_type,
            "domain": domain,
            "records": records,
            "response_time_ms": round((end_time - start_time) * 1000, 2),
            "nameserver": str(resolver.nameservers[0]) if resolver.nameservers else None
        }
        
    except dns.resolver.NXDOMAIN:
        return {
            "success": False,
            "error": "Domain does not exist (NXDOMAIN)",
            "record_type": record_type,
            "domain": domain
        }
    except dns.resolver.NoAnswer:
        return {
            "success": False,
            "error": f"No {record_type} records found",
            "record_type": record_type,
            "domain": domain
        }
    except dns.resolver.Timeout:
        return {
            "success": False,
            "error": "DNS query timeout",
            "record_type": record_type,
            "domain": domain
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"DNS lookup failed: {str(e)}",
            "record_type": record_type,
            "domain": domain
        }

def run_dns_full_lookup(domain: str) -> Dict[str, Any]:
    """Выполняет полный DNS lookup (все типы записей)"""
    results = {}
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
    
    for record_type in record_types:
        result = run_dns_lookup(domain, record_type)
        results[record_type] = result
    
    return {
        "success": True,
        "domain": domain,
        "lookups": results
    }

# ============= OTHER CHECK FUNCTIONS =============

def run_ping(target: str) -> str:
    """Выполняет команду ping"""
    is_windows = sys.platform.startswith('win')
    cmd = ['ping', '-n' if is_windows else '-c', '4', target]
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        end_time = time.time()
        
        # Parse ping statistics
        output = result.stdout.strip()
        
        return json.dumps({
            "success": result.returncode == 0,
            "output": output,
            "response_time_ms": round((end_time - start_time) * 1000, 2)
        })
    except subprocess.TimeoutExpired:
        return json.dumps({
            "success": False,
            "error": "Ping timeout (15s)",
            "response_time_ms": 15000
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Ping failed: {str(e)}"
        })

def run_traceroute(target: str) -> str:
    """Выполняет команду traceroute"""
    is_windows = sys.platform.startswith('win')
    cmd = ['tracert'] if is_windows else ['traceroute', '-m', '20']
    cmd.append(target)
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        end_time = time.time()
        
        return json.dumps({
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "response_time_ms": round((end_time - start_time) * 1000, 2)
        })
    except subprocess.TimeoutExpired:
        return json.dumps({
            "success": False,
            "error": "Traceroute timeout (30s)"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Traceroute failed: {str(e)}"
        })

def run_tcp_connect(target: str, port: int) -> str:
    """Пытается установить TCP-соединение"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    try:
        start_time = time.time()
        sock.connect((target, port))
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        
        return json.dumps({
            "success": True,
            "port": port,
            "status": "open",
            "response_time_ms": response_time
        })
    except socket.timeout:
        return json.dumps({
            "success": False,
            "port": port,
            "status": "timeout",
            "error": "Connection timeout"
        })
    except ConnectionRefusedError:
        return json.dumps({
            "success": False,
            "port": port,
            "status": "closed",
            "error": "Connection refused"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "port": port,
            "status": "error",
            "error": str(e)
        })
    finally:
        sock.close()

def run_http_check(url: str) -> str:
    """Выполняет HTTP GET запрос"""
    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        
        start_time = time.time()
        response = requests.get(url, timeout=10, allow_redirects=True, verify=False)
        end_time = time.time()
        
        response_data = {
            "success": True,
            "status_code": response.status_code,
            "response_time_ms": round((end_time - start_time) * 1000, 2),
            "headers": dict(list(response.headers.items())[:20]),  # Limit headers
            "url": response.url,
            "redirects": len(response.history)
        }
        
        return json.dumps(response_data)
        
    except requests.exceptions.Timeout:
        return json.dumps({
            "success": False,
            "error": "HTTP request timeout (10s)"
        })
    except requests.exceptions.ConnectionError:
        return json.dumps({
            "success": False,
            "error": "Connection error - host unreachable"
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "success": False,
            "error": f"HTTP request failed: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        })

# ============= TASK PROCESSING =============

def send_result_to_server(report_data: dict):
    """Отправляет результат на основной сервер"""
    result_endpoint = f"{MAIN_SERVER_URL}/api/v1/results"
    
    try:
        response = requests.post(
            result_endpoint, 
            json=report_data, 
            timeout=10,
            headers={"Authorization": f"Bearer {AGENT_API_TOKEN}"} if AGENT_API_TOKEN else {}
        )
        response.raise_for_status()
        print(f"✅ Result sent for task {report_data.get('taskUIID')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending result: {e}")
        return False

def process_task(task_data: dict):
    """Обрабатывает задачу проверки"""
    global active_tasks
    
    with task_lock:
        active_tasks += 1
    
    try:
        task_uuid = task_data.get("taskUIID") or task_data.get("check_id")
        check_type = task_data.get("check_type")
        target = task_data.get("target")
        
        print(f"🔄 Processing task {task_uuid}: {check_type} -> {target}")
        
        result_content = ""
        
        # Execute check based on type
        try:
            if check_type in ["http", "https"]:
                result_content = run_http_check(target)
                
            elif check_type == "ping":
                result_content = run_ping(target)
                
            elif check_type == "traceroute":
                result_content = run_traceroute(target)
                
            elif check_type == "tcp" or check_type == "tcp-port":
                if ":" in target:
                    host, port_str = target.rsplit(":", 1)
                    port = int(port_str)
                else:
                    host = target
                    port = 80
                result_content = run_tcp_connect(host, port)
                
            elif check_type == "dns":
                # Full DNS lookup (all record types)
                result = run_dns_full_lookup(target)
                result_content = json.dumps(result)
                
            elif check_type.startswith("dns-"):
                # Specific DNS record type
                record_type = check_type.split("-")[1].upper()
                result = run_dns_lookup(target, record_type)
                result_content = json.dumps(result)
                
            else:
                result_content = json.dumps({
                    "success": False,
                    "error": f"Unsupported check type: {check_type}"
                })
                
        except Exception as e:
            result_content = json.dumps({
                "success": False,
                "error": f"Critical error during task execution: {str(e)}"
            })
        
        # Send result to server
        report_data = {
            "country": AGENT_COUNTRY,
            "UIID": AGENT_UIID,
            "taskUIID": task_uuid,
            "task": check_type,
            "target": target,
            "result": result_content
        }
        
        send_result_to_server(report_data)
        
    finally:
        with task_lock:
            active_tasks -= 1

# ============= TASK POLLING =============

def task_poller():
    """Опрашивает сервер на наличие новых задач"""
    print("📡 Task poller started")
    
    consecutive_errors = 0
    
    while not stopper.is_set():
        try:
            # Check if we can accept more tasks
            with task_lock:
                if active_tasks >= MAX_CONCURRENT_TASKS:
                    print(f"⏳ Max concurrent tasks reached ({MAX_CONCURRENT_TASKS}), waiting...")
                    stopper.wait(2)
                    continue
            
            # Poll for tasks
            response = requests.get(
                f"{MAIN_SERVER_URL}/api/agents/{AGENT_UIID}/tasks",
                params={"limit": MAX_CONCURRENT_TASKS - active_tasks},
                timeout=10,
                headers={"Authorization": f"Bearer {AGENT_API_TOKEN}"} if AGENT_API_TOKEN else {}
            )
            
            if response.status_code == 200:
                data = response.json()
                tasks = data.get("tasks", [])
                
                if tasks:
                    print(f"📥 Received {len(tasks)} task(s)")
                    for task in tasks:
                        # Start task in separate thread
                        threading.Thread(target=process_task, args=(task,), daemon=True).start()
                    consecutive_errors = 0
                    
            else:
                print(f"⚠️ Server returned status {response.status_code}")
                consecutive_errors += 1
                
        except requests.exceptions.RequestException as e:
            consecutive_errors += 1
            if consecutive_errors <= 3:
                print(f"❌ Error polling tasks: {e}")
            
            # Exponential backoff on errors
            if consecutive_errors > 5:
                stopper.wait(min(30, POLL_INTERVAL * 2 ** (consecutive_errors - 5)))
            
        except Exception as e:
            print(f"💥 Unexpected error in poller: {e}")
        
        # Wait before next poll
        stopper.wait(POLL_INTERVAL)
    
    print("📡 Task poller stopped")

def heartbeat_sender():
    """Отправляет heartbeat на сервер"""
    print("💓 Heartbeat sender started")
    
    while not stopper.is_set():
        try:
            response = requests.post(
                f"{MAIN_SERVER_URL}/api/agents/heartbeat",
                json={"agent_id": AGENT_UIID},
                timeout=5,
                headers={"Authorization": f"Bearer {AGENT_API_TOKEN}"} if AGENT_API_TOKEN else {}
            )
            
            if response.status_code == 200:
                print("💓 Heartbeat sent")
            else:
                print(f"⚠️ Heartbeat failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Heartbeat error: {e}")
        
        stopper.wait(30)  # Send heartbeat every 30 seconds
    
    print("💓 Heartbeat sender stopped")

# ============= FASTAPI ENDPOINTS =============

@app.on_event("startup")
async def start_background_workers():
    """Запуск фоновых потоков"""
    print(f"🚀 Agent starting: {AGENT_NAME} ({AGENT_COUNTRY})")
    print(f"🎯 Main server: {MAIN_SERVER_URL}")
    print(f"🆔 Agent ID: {AGENT_UIID}")
    
    # Start task poller
    threading.Thread(target=task_poller, daemon=True).start()
    
    # Start heartbeat sender
    threading.Thread(target=heartbeat_sender, daemon=True).start()
    
    print("✅ Agent started successfully")

@app.on_event("shutdown")
async def stop_background_workers():
    """Остановка фоновых потоков"""
    print("🛑 Agent shutting down...")
    stopper.set()

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return Response(
        status_code=200,
        content=json.dumps({
            "status": "healthy",
            "agent": AGENT_NAME,
            "location": AGENT_COUNTRY,
            "agent_id": AGENT_UIID,
            "active_tasks": active_tasks,
            "max_concurrent_tasks": MAX_CONCURRENT_TASKS
        }),
        media_type="application/json"
    )

@app.get("/stats")
async def get_stats():
    """Agent statistics"""
    return {
        "agent_id": AGENT_UIID,
        "name": AGENT_NAME,
        "location": AGENT_COUNTRY,
        "active_tasks": active_tasks,
        "max_concurrent_tasks": MAX_CONCURRENT_TASKS,
        "main_server": MAIN_SERVER_URL
    }

@app.post("/check")
async def check_task_direct(req_data: CheckRequest):
    """
    Принимает задачу напрямую (для обратной совместимости)
    В production используется polling через /api/agents/{id}/tasks
    """
    task_data = req_data.dict()
    print(f"📥 Received direct task: {task_data.get('taskUIID')}")
    
    try:
        threading.Thread(target=process_task, args=(task_data,), daemon=True).start()
        return {"status": "accepted", "message": "Task dispatched for processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start task: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

