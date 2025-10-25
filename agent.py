from fastapi import FastAPI, Response, Request, HTTPException
from pydantic import BaseModel
import threading
import json
import time
import subprocess
import requests
import socket
import uuid
import sys # Импорт для проверки ОС

# --- Конфигурация ---
MAIN_SERVER_URL = "http://localhost:8000" # Замените на фактический адрес вашего main_server
TASK_QUEUE_ENDPOINT = f"{MAIN_SERVER_URL}/api/v1/tasks" # API для получения задач с сервера
AGENT_COUNTRY = "Russia" # Замените на реальное определение GeoIP или конфигурацию
POLLING_INTERVAL_SECONDS = 5 # Интервал опроса сервера на наличие новых задач

app = FastAPI()

# Используется для остановки фонового потока при завершении работы
stopper = threading.Event()

# Модель для входящего запроса на проверку (используется для унификации)
class CheckRequest(BaseModel):
    task_uuid: str
    check_type: str
    target: str

# --- Вспомогательные функции для выполнения проверок ---

# ВНИМАНИЕ: Команды 'ping' и 'traceroute' зависят от ОС. 
# На Linux: ping -c, traceroute
# На Windows: ping -n, tracert

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

# --- Функция получения задачи ---

def fetch_task_from_server() -> dict | None:
    """
    Выполняет GET-запрос к бэкенду для получения одной задачи из очереди.
    """
    try:
        # В реальной системе здесь может потребоваться токен агента
        response = requests.get(TASK_QUEUE_ENDPOINT, timeout=3)
        response.raise_for_status() 
        
        # Ожидаем, что сервер вернет JSON с одной задачей или пустой JSON/204 No Content
        data = response.json()
        
        # Сервер может вернуть {"task_uuid": "...", "check_type": "...", "target": "..."}
        if data and isinstance(data, dict) and data.get("task_uuid"):
            return data
            
        return None # Нет задач
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: Task endpoint {TASK_QUEUE_ENDPOINT} not found. Check main server.")
        elif e.response.status_code == 204: # No Content - ожидаемый ответ при пустой очереди
            return None
        else:
             print(f"HTTP Error fetching task: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        # Ошибка соединения
        print(f"Connection Error fetching task: {e}")
        return None
    except Exception as e:
        # Ошибка парсинга JSON
        print(f"Unexpected error fetching task: {e}")
        return None

# --- Функция отправки результата на сервер ---

def send_result_to_server(report_data: dict):
    """Отправляет результат проверки на основной сервер."""
    result_endpoint = f"{MAIN_SERVER_URL}/api/v1/results" 
    print(f"Sending result for UUID {report_data.get('UIID')}")
    try:
        response = requests.post(result_endpoint, json=report_data, timeout=5)
        response.raise_for_status() 
        print(f"Result sent successfully. Server response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending result to main server: {e}")

# --- Основная логика агента (многопоточная очередь) ---

def process_task(task_data: dict):
    """Выполняет проверку и отправляет результат."""
    
    task_uuid = task_data.get("task_uuid")
    check_type = task_data.get("check_type")
    target = task_data.get("target")

    result_content = f"Error: Task {task_uuid} not processed."
    
    # 2. Выполнение проверки (логика осталась та же)
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
        # TODO: Добавить run_dns_lookup (A, AAAA, MX, NS, TXT) [cite: 24]
        else:
            result_content = f"Unsupported check type: {check_type}"
            
    except Exception as e:
        result_content = f"Critical error during task execution: {e}"

    # 3. Формирование отчета
    report_data = {
        "country": AGENT_COUNTRY,
        "UIID": task_uuid,
        "task": check_type,
        "result": result_content
    }

    # 4. Отправка результата на сервер
    send_result_to_server(report_data)


def task_dispatcher():
    """
    Фоновый поток для опроса сервера на наличие задач и их диспетчеризации.
    Реализует многопоточную очередь: опрос -> получение -> запуск в новом потоке.
    """
    print(f"--- Task Dispatcher started. Polling server every {POLLING_INTERVAL_SECONDS} seconds ---")
    while not stopper.is_set():
        
        # 1. Опрос сервера
        task_from_server = fetch_task_from_server()
        
        if task_from_server:
            print(f"Task received (UUID: {task_from_server.get('task_uuid')}). Dispatching...")
            # 2. Запуск обработки в отдельном потоке (многопоточная очередь)
            threading.Thread(target=process_task, args=(task_from_server,), daemon=True).start()
        else:
            print(f"No new tasks found on server at {TASK_QUEUE_ENDPOINT}.")
            
        # 3. Ожидание до следующего опроса
        # Используем stopper.wait() для неблокирующего ожидания, которое можно прервать при shutdown
        stopper.wait(POLLING_INTERVAL_SECONDS)
        
    print("--- Task Dispatcher stopped ---")

# --- Маршруты FastAPI ---

@app.on_event("startup")
async def start_async_worker():
    """Запуск фонового потока для обработки задач при старте приложения."""
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

# Маршрут для POST /check можно оставить как запасной или убрать, 
# если весь функционал перенесен на опрос (polling)
# В данной реализации основной механизм получения задач - task_dispatcher (polling).
@app.post("/check")
async def check_task_direct(req_data: CheckRequest):
    """Принимает задачу напрямую (без очереди) и запускает ее обработку."""
    task_data = req_data.dict()
    print(f"Received direct task: {task_data}")
    try:
        threading.Thread(target=process_task, args=(task_data,), daemon=True).start()
        return {"status": "success", "message": "Direct task accepted and dispatched for processing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start task processing: {e}")