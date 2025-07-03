from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client['file_sharing_app']
users_collection = db['users']
files_collection = db['files']
