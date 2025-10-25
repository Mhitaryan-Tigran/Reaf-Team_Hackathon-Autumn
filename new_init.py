import uuid
import socket
import urllib.request
import json

agentUUID = str(uuid.uuid4())


def get_public_ip(timeout=5):
    """Return the public IP (via ipify) or fall back to the local hostname IP."""
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
    """Return (country, region) for the given IP using ip-api.com. Returns (None, None) on failure."""
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


# Determine IP and geo information
ip = get_public_ip()
country, region = geo_ip_lookup(ip)


# Write agentUUID and country into .env
with open(".env", "w") as f:
    f.write(f"agentUUID={agentUUID}\n")
    # write country even if blank so .env keys exist predictably
    f.write(f"country={country or ''}\n")


# Print results
print(f"IP: {ip}")
print(agentUUID)
print(f"Country: {country}")
print(f"Region: {region}")


# Print an SQL statement that can be used to insert this agent into the DB.
# Use single quotes around string values so the statement is valid SQL.
print(f"INSERT INTO Agents (ip, UIID) VALUES ('{ip}', '{agentUUID}');")
