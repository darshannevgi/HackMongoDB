from db.client import db
from embeddings.voyage import embed
from datetime import datetime

def write_context(task_id, agent_id, content):
    db.shared_context.insert_one({
        "taskId": task_id,
        "agentId": agent_id,
        "content": content,
        "embedding": embed(content),
        "timestamp": datetime.utcnow()
    })

def retrieve_context(query, limit=5):
    results = db.shared_context.aggregate([
        {
            "$vectorSearch": {
                "index": "shared_context_index",
                "queryVector": embed(query),
                "path": "embedding",
                "limit": limit,
                "numCandidates": 10,
            }
        }
    ])
    return list(results)
