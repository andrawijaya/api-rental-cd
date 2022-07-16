from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config


def connect(collection_Name):
    mongodb_url = config("DB_URI")
    mongodb_name = config("DB_NAME")
    try:
        client = AsyncIOMotorClient(mongodb_url)

        assert client is not None
        print(f"Connected to MongoDB at {mongodb_url}")
        db = client[f"{mongodb_name}"]
        collection = db[collection_Name]
        return collection
    except Exception as e:
        print("Error: " + str(e))
        return None


connect('users')
