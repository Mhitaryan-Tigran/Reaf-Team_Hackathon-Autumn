import uuid
import socket
import urllib.request
import json

agentUUID = str(uuid.uuid4())


def get_public_ip(timeout=5):
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=timeout) as r:
            data = json.load(r)
            return data.get("ip")
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None


def geo_ip_lookup(ip, timeout=5):
    if not ip:
        return None, None
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,message"
        with urllib.request.urlopen(url, timeout=timeout) as r:
            data = json.load(r)
            if data.get("status") == "success":
                return data.get("country"), data.get("regionName")
    except Exception:
        pass
    return None, None


ip = get_public_ip()
country, region = geo_ip_lookup(ip)


with open(".env", "w") as f:
    f.write(f"agentUUID={agentUUID}\n")
    f.write(f"country={country or ''}\n")
    f.write(f"masterIPandPort={input("Введите ip:порт основного сервера: ")}\n")


print(f"IP: {ip}")
print(agentUUID)
print(f"Country: {country}")
print(f"Region: {region}")


print(f"INSERT INTO Agents (ip, UIID) VALUES ('{ip}', '{agentUUID}');")
