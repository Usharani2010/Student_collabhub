from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://usharaniborigi10:uNlmL5fWkHW59QOz@projects-cluster.wxe6nyl.mongodb.net/?retryWrites=true&w=majority&appName=projects-cluster")

db= client["student_collaboration_hub"]
print("Connected to database:", db.name)
