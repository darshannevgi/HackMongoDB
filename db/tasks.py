from db.client import db
from datetime import datetime

def create_task(task_id, agent_id, objective, embedding):
    db.tasks.insert_one({
        "taskId": task_id,
        "objective": objective,
        "assignedAgent": agent_id,
        "status": "pending",
        "createdAt": datetime.utcnow()
    })
    print("Created tasks and inserted in DB Successfully :", task_id, "Objective:", objective)



def fetch_next_task(agent_id: str):
    """
    Atomically fetch the next pending task for the agent.
    Marks the task as 'in_progress' to prevent duplicates.
    """
    task = db.tasks.find_one_and_update(
        {"assignedAgent": agent_id, "status": "pending"},
        {"$set": {"status": "in_progress"}},
        sort=[("createdAt", 1)]
    )
    return task

def complete_task(task_id):
    db.tasks.update_one(
        {"taskId": task_id},
        {"$set": {"status": "complete"}}
    )