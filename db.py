from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None

def get_database():
    global client, db
    if client is None:
        client = AsyncIOMotorClient("mongodb+srv://usharaniborigi10:uNlmL5fWkHW59QOz@projects-cluster.wxe6nyl.mongodb.net/?retryWrites=true&w=majority&appName=projects-cluster")
        db = client["student_collaboration_hub"]
    return db
