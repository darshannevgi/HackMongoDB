from db.tasks import fetch_next_task, complete_task
from db.shared_context import write_context, retrieve_context
from openai import OpenAI
import os

AGENT_ID = "market_intel_agent"

# Fireworks client
fireworks = OpenAI(
    api_key="fw_2vKeHWeZyu99qXudDFe9ww",
    base_url="https://api.fireworks.ai/inference/v1"
)

def analyze_market(objective: str, existing_context: list) -> str:
    """
    Uses Fireworks AI to analyze market intelligence.
    """
    context_text = "\n".join(f"- {i['content']}" for i in existing_context)
    prompt = f"""
You are a Market Intelligence agent.
Objective: {objective}
Prior insights: {context_text}

Provide a concise analysis of the market, trends, and recommendations.
"""
    response = fireworks.chat.completions.create(
        model="accounts/fireworks/models/deepseek-r1-0528",  # replace with valid accessible model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content

def run():
    while True:
        task = fetch_next_task(AGENT_ID)
        print(f"[market_intel_agent] task fetched:", task)
        if not task:
            break

        task_id = task["taskId"]
        objective = task["objective"]
        print(task)
        prior_context = retrieve_context(objective, limit=3)
        result = analyze_market(objective, prior_context)
        print(result)
        write_context(task_id, AGENT_ID, result)

        complete_task(task_id)
        print(f"[Market Agent] Completed task: {task_id}")
