import uuid

with open(".env", "w") as f:
    f.write(f"agentUUID={str(uuid.uuid4())}")