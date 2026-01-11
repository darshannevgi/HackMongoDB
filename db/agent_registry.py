from db.client import db
from embeddings.voyage import embed
from datetime import datetime

from db.client import db
from embeddings.voyage import embed
from datetime import datetime

def register_agent(agent_id, role, description, skills):
    db.agents.update_one(
        {"_id": agent_id},
        {
            "$setOnInsert": {
                "role": role,
                "description": description,
                "skills": skills,
                "availability": "idle",
                "embedding": embed(
                    f"{role} {description} {' '.join(skills)}"
                ),
                "createdAt": datetime.utcnow()
            }
        },
        upsert=True
    )

def discover_agent(task_description: str, limit=1):
    results = db.agents.aggregate([
        {
            "$vectorSearch": {
                "index": "agent_embedding_index",
                "queryVector": embed(task_description),
                "path": "embedding",
                "numCandidates": 10,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 1,
                "role": 1,
                "skills": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ])

    return list(results)
