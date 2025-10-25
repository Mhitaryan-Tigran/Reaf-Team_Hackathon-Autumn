from fastapi import FastAPI, Response, Request, HTTPException
from pydantic import BaseModel
import threading
import json
import time
import subprocess
import requests
import socket
import uuid

# --- Конфигурация ---
MAIN_SERVER_URL = "http://localhost:8000" # Замените на фактический адрес вашего main_server
AGENT_COUNTRY = "Russia" # Замените на реальное определение GeoIP или конфигурацию

app = FastAPI()

# Используется для остановки фонового потока при завершении работы
stopper = threading.Event()

# Модель для входящего запроса на проверку
class CheckRequest(BaseModel):
    # UUIDv4 задачи, по которому будет отправляться результат
    task_uuid: str
    # Тип проверки (http, https, ping, tcp-port, traceroute, dns)
    check_type: str
    # Хост для проверки (URL, IP, домен или IP:порт)
    target: str

# --- Вспомогательные функции для выполнения проверок ---

def run_ping(target: str) -> str:
    """Выполняет команду ping и возвращает результат."""
    try:
        # -c 4: 4 пакета (Linux); -n 4: 4 пакета (Windows)
        result = subprocess.run(['ping', '-c', '4', target], capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing ping: {e}"

def run_traceroute(target: str) -> str:
    """Выполняет команду traceroute и возвращает результат."""
    try:
        # -q 1: 1 запрос на каждый хоп (Linux); tracert -d (Windows)
        # В реальном проекте лучше использовать специализированные библиотеки.
        result = subprocess.run(['traceroute', target], capture_output=True, text=True, timeout=20)
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
        # Добавляем схему, если она отсутствует
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
    # Адрес для отправки результатов (должен быть реализован на main_server.py)
    result_endpoint = f"{MAIN_SERVER_URL}/api/v1/results" 
    print(f"Sending result to {result_endpoint}: {report_data}")
    try:
        response = requests.post(result_endpoint, json=report_data, timeout=5)
        response.raise_for_status() # Вызывает ошибку для плохих статусов (4xx, 5xx)
        print(f"Result sent successfully. Server response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending result to main server: {e}")

# --- Основная логика агента (многопоточная очередь) ---

def process_task(task_data: dict):
    """Выполняет проверку и отправляет результат."""
    
    # 1. Распаковка данных
    task_uuid = task_data.get("task_uuid")
    check_type = task_data.get("check_type")
    target = task_data.get("target")

    # 2. Выполнение проверки
    result_content = "Unknown check type or execution error."
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
        # TODO: Добавить run_dns_lookup
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
    """Симулирует многопоточную очередь: ждет новые задачи и запускает их в отдельном потоке."""
    # В реальном проекте эта функция опрашивала бы Redis/RabbitMQ на наличие новых задач.
    print("--- Task Dispatcher (Async Worker) started ---")
    while not stopper.is_set():
        # Симуляция проверки очереди каждые 5 секунд
        # (Здесь должна быть реальная логика получения задачи из очереди)
        
        # Заглушка: если бы мы получили задачу из очереди, мы бы ее обработали:
        # Example: task_from_queue = get_task_from_queue()
        # if task_from_queue:
        #     # Запускаем обработку задачи в отдельном потоке
        #     threading.Thread(target=process_task, args=(task_from_queue,), daemon=True).start()
            
        time.sleep(5)
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

# 1. Отвечать на live запрос который находится по /
@app.get("/")
async def live():
    """Проверка доступности агента (Heartbeat)."""
    return Response(status_code=200, content=f"Agent is alive and running in {AGENT_COUNTRY}.")

# 2. POST запрос на выполнение (http, https, ping, tcp-порт, traceroute) по ip или домену
@app.post("/check")
async def check_task(req_data: CheckRequest):
    """
    Принимает задачу от бэкенда и запускает ее обработку в отдельном потоке.
    Это симуляция немедленного приема задачи из очереди.
    """
    
    # Преобразуем Pydantic модель в словарь
    task_data = req_data.dict()
    print(f"Received new task: {task_data}")

    # Запускаем обработку задачи в отдельном потоке
    # (Это и есть ваша многопоточная очередь: быстрый прием + асинхронная обработка)
    try:
        threading.Thread(target=process_task, args=(task_data,), daemon=True).start()
        return {"status": "success", "message": "Task accepted and dispatched for processing."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start task processing: {e}")