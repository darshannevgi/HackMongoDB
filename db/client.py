import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
import certifi

# Get the path to the certifi CA bundle
ca = certifi.where()
#ATLAS_URI = "mongodb+srv://darshannevgi_db_hack:Alborada123@cluster0.18kljc.mongodb.net/?appName=Cluster0"
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

print("Attempting")
client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=ca)
db = client.agentic_system
print("Connected to Atlas instance! We are good to go!")