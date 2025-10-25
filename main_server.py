from fastapi import FastAPI, Response, Request, HTTPException
from pydantic import BaseModel
import threading
import json
import time
import subprocess
import requests
import socket
import sys 

# --- Конфигурация ---
MAIN_SERVER_URL = "http://localhost:8000" # Адрес, куда агент отправляет результаты
AGENT_COUNTRY = "Russia" # Страна, откуда работает агент
AGENT_UIID = "agent-482a-9f5b" # Уникальный ID агента (UIID)

app = FastAPI()

# Используется для остановки фонового потока при завершении работы
stopper = threading.Event()

# Модель для входящего запроса на проверку от main-server
class CheckRequest(BaseModel):
    # Идентификатор задачи, который нужно вернуть обратно
    taskUIID: str 
    # Тип проверки (http, https, ping, tcp-port, traceroute)
    check_type: str
    # Хост для проверки (URL, IP, домен или IP:порт)
    target: str

# --- Вспомогательные функции для выполнения проверок ---

# (Логика run_ping, run_traceroute, run_tcp_connect, run_http_check остается без изменений)

def run_ping(target: str) -> str:
    """Выполняет команду ping и возвращает результат."""
    is_windows = sys.platform.startswith('win')
    cmd = ['ping', '-n' if is_windows else '-c', '4', target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing ping: {e}"

def run_traceroute(target: str) -> str:
    """Выполняет команду traceroute и возвращает результат."""
    is_windows = sys.platform.startswith('win')
    cmd = ['tracert'] if is_windows else ['traceroute']
    cmd.append(target)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing traceroute: {e}"

def run_tcp_connect(target: str, port: int) -> str:
    """Пытается установить TCP-соединение на указанный порт."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        start_time = time.time()
        sock.connect((target, port))
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        return f"Connection successful. Response time: {response_time} ms."
    except Exception as e:
        return f"Connection failed: {e}"
    finally:
        sock.close()

def run_http_check(url: str) -> str:
    """Выполняет HTTP GET запрос и возвращает статус, заголовки и время."""
    try:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
            
        start_time = time.time()
        response = requests.get(url, timeout=10, allow_redirects=False)
        end_time = time.time()
        
        response_data = {
            "status_code": response.status_code,
            "response_time_ms": round((end_time - start_time) * 1000, 2),
            "headers": dict(response.headers)
        }
        return json.dumps(response_data, indent=2)
    except requests.exceptions.RequestException as e:
        return f"HTTP/S check failed: {e}"
    except Exception as e:
        return f"Error during HTTP/S check: {e}"

# --- Функция отправки результата на сервер ---

def send_result_to_server(report_data: dict):
    """Отправляет результат проверки на основной сервер."""
    # Эндпоинт, который должен принимать результат на main_server.py
    result_endpoint = f"{MAIN_SERVER_URL}/api/v1/results" 
    print(f"Sending result for taskUIID: {report_data.get('taskUIID')}")
    try:
        response = requests.post(result_endpoint, json=report_data, timeout=5)
        response.raise_for_status() 
        print(f"Result sent successfully. Server response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending result to main server: {e}")

# --- Основная логика агента (многопоточная обработка) ---

def process_task(task_data: dict):
    """Выполняет проверку и отправляет результат."""
    
    # 1. Распаковка данных (используем taskUIID)
    task_uuid = task_data.get("taskUIID")
    check_type = task_data.get("check_type")
    target = task_data.get("target")

    result_content = f"Error: Task {task_uuid} not processed."
    
    # 2. Выполнение проверки 
    try:
        if check_type in ["http", "https"]:
            result_content = run_http_check(target)
        elif check_type == "ping":
            result_content = run_ping(target)
        elif check_type == "traceroute":
            result_content = run_traceroute(target)
        elif check_type == "tcp-port":
            if ":" in target:
                host, port_str = target.split(":")
                port = int(port_str)
                result_content = run_tcp_connect(host, port)
            else:
                result_content = "TCP-port check requires target in format 'host:port'."
        else:
            result_content = f"Unsupported check type: {check_type}"
            
    except Exception as e:
        result_content = f"Critical error during task execution: {e}"

    # 3. Формирование отчета в требуемом формате
    report_data = {
        "country": AGENT_COUNTRY,
        "UIID": AGENT_UIID, # Идентификатор агента
        "taskUIID": task_uuid, # Идентификатор задачи
        "task": check_type,
        "target": target, # Возвращаем target
        "result": result_content
    }

    # 4. Отправка результата на сервер
    send_result_to_server(report_data)


def task_dispatcher():
    """Заглушка для фонового потока. 
    Многопоточность для задач обеспечивается через threading.Thread в /check.
    """
    print("--- Task Dispatcher (Heartbeat placeholder) started ---")
    while not stopper.is_set():
        # Здесь может быть логика отправки Heartbeat на сервер
        # print("Agent is sending heartbeat...") 
        stopper.wait(5)
    print("--- Task Dispatcher stopped ---")

# --- Маршруты FastAPI ---

@app.on_event("startup")
async def start_async_worker():
    """Запуск фонового потока при старте приложения."""
    backgroundTask = threading.Thread(target=task_dispatcher, daemon=True)
    backgroundTask.start()
    print("Agent started and background dispatcher thread initiated.")

@app.on_event("shutdown")
async def stop_async_worker():
    """Остановка фонового потока при завершении работы."""
    stopper.set()
    print("Agent shutdown signal sent.")

@app.get("/")
async def live():
    """Проверка доступности агента (Heartbeat)."""
    return Response(status_code=200, content=f"Agent is alive and running in {AGENT_COUNTRY}.")

@app.post("/check")
async def check_task_direct(req_data: CheckRequest):
    """
    Принимает задачу напрямую от main-server и запускает ее обработку
    в отдельном потоке (реализация многопоточной очереди).
    """
    task_data = req_data.dict()
    print(f"Received task (taskUIID: {task_data.get('taskUIID')}). Dispatching...")
    
    # Запуск обработки задачи в отдельном потоке
    try:
        threading.Thread(target=process_task, args=(task_data,), daemon=True).start()
        return {"status": "success", "message": "Task accepted and dispatched for processing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start task processing: {e}")