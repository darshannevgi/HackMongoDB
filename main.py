from agents.bootstrap_agents import bootstrap_agents
from agents.planner import plan_launch
from agents.run_agents import run_all_agents
from agents.launch_lead import run as lead_run
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    bootstrap_agents()
    plan_launch("We want to launch a new smart fitness wearable for teenagers in North America. Please analyze market demand, competitor pricing, and operational feasibility, and provide a recommendation on whether we should proceed with the launch.")
    run_all_agents()
    lead_run()




'''
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import certifi
load_dotenv()
ca = certifi.where()
class AtlasClient:

    def __init__(self, altas_uri, dbname):
        self.mongodb_client = MongoClient(altas_uri, tlsCAFile=ca)
        self.database = self.mongodb_client[dbname]

    # A quick way to test if we can connect to Atlas instance
    def ping(self):
        self.mongodb_client.admin.command("ping")

    # Get the MongoDB Atlas collection to connect to
    def get_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    # Query a MongoDB collection
    def find(self, collection_name, filter={}, limit=0):
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items
ATLAS_URI = "mongodb+srv://darshannevgi_db_hack:Alborada123@cluster0.18kljc.mongodb.net/?appName=Cluster0"
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
print("Started")
DB_NAME = "sample_mflix"
atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()
print("Connected to Atlas instance! We are good to go!")
'''
#
'''
agentic_launch/
├── agents/
│   ├── planner.py
│   ├── market_agent.py
│   ├── pricing_agent.py
├── db/
│   ├── client.py
│   ├── agent_registry.py
│   ├── tasks.py
│   └── shared_context.py
├── embeddings/
│   └── voyage.py
├── main.py
└── .env

from pymongo import MongoClient


class AtlasClient:

    def __init__(self, altas_uri, dbname):
        self.mongodb_client = MongoClient(altas_uri)
        self.database = self.mongodb_client[dbname]

    # A quick way to test if we can connect to Atlas instance
    def ping(self):
        self.mongodb_client.admin.command("ping")

    # Get the MongoDB Atlas collection to connect to
    def get_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    # Query a MongoDB collection
    def find(self, collection_name, filter={}, limit=0):
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items

DB_NAME = "sample_mflix"
COLLECTION_NAME = "embedded_movies"
DB_NAME = "sample_mflix"
atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()
print("Connected to Atlas instance! We are good to go!")

'''