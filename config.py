import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "fernet-key-32bitneeded")  # Must be 32 url-safe base64-encoded bytes
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
