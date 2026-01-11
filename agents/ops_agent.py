from db.tasks import fetch_next_task, complete_task
from db.shared_context import write_context, retrieve_context
from openai import OpenAI
import os

AGENT_ID = "ops_agent"

# Initialize Fireworks AI client
fireworks = OpenAI(
    api_key=os.getenv("FIREWORKS_API_KEY"),
    base_url="https://api.fireworks.ai/inference/v1"
)
def analyze_ops(objective: str, existing_context: list) -> str:
    """
    Uses Fireworks AI to generate an operational feasibility analysis.
    """
    context_text = "\n".join(f"- {i['content']}" for i in existing_context)
    prompt = f"""
You are an Operations Agent.
Objective: {objective}
Prior insights: {context_text}

Provide a concise assessment of operational feasibility, 
required resources, potential risks, and recommendations.
"""
    response = fireworks.chat.completions.create(
        model="accounts/fireworks/models/deepseek-r1-0528",  # replace with your accessible model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content

def run():
    """
    Main agent loop: fetch tasks, analyze, write results, mark complete.
    """
    while True:
        task = fetch_next_task(AGENT_ID)
        if not task:
            break

        task_id = task["taskId"]
        objective = task["objective"]
        print("Ops Agent", objective)
        #objective = objective['objective']
        # Pull relevant prior insights for context
        prior_context = retrieve_context(objective, limit=3)

        # Generate operational analysis using LLM
        result = analyze_ops(objective, prior_context)
        print(result)
        # Write insights to shared context
        write_context(task_id, AGENT_ID, result)

        # Mark task complete
        complete_task(task_id)

        print(f"[Ops Agent] Completed task: {task_id}")
