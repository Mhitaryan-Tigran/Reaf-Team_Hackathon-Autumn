import uuid
import socket

agentUUID = str(uuid.uuid4())

with open(".env", "w") as f:
    f.write(f"agentUUID={agentUUID}")

print(f"IP: {socket.gethostbyname(socket.gethostname())}")
print(agentUUID)
