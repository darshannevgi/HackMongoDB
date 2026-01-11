import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
load_dotenv()
ca = certifi.where()
ATLAS_URI = "mongodb+srv://darshannevgi_db_hack:Alborada123@cluster0.18kljc.mongodb.net/?appName=Cluster0"
client = MongoClient(ATLAS_URI, tlsCAFile=ca)
db = client.agentic_system

# dummy vector with correct dimension
dummy_vector = [0.01] * 1536

results = list(
    db.agents.aggregate([
        {
            "$vectorSearch": {
                "index": "agent_embedding_index",
                "queryVector": dummy_vector,
                "path": "embedding",
                "numCandidates": 50,
                "limit": 1
            }
        }
    ])
)

print("Vector search results:", results)
