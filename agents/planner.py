import os
import uuid
from typing import List, Dict

from openai import OpenAI

from db.tasks import create_task
import json

# OPTIONAL: if you want to store embeddings for tasks
# Comment these 2 lines if you don't want task embeddings.
from embeddings.voyage import embed as voyage_embed


PLANNER_MODEL = "gpt-4o-mini"
OPENAI_API_KEY = "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"

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Export it in your environment.")

client = OpenAI(api_key=OPENAI_API_KEY)
def plan_launch(user_prompt: str) -> List[Dict]:
    """
    Planner agent:
    - Takes user_prompt
    - Uses OpenAI to produce EXACTLY 3 tasks (market/pricing/ops) as JSON
    - Creates tasks in MongoDB
    - Returns tasks for logging
    """
    print("📝 Planner: generating tasks...")

    planner_prompt = f"""
Return ONLY valid JSON (no markdown, no explanation, no extra text).

Create EXACTLY 3 tasks, one per agent below:
- market_intel_agent: market demand, customer segments, trends
- pricing_agent: competitor pricing, monetization, price recommendation
- ops_agent: feasibility, resources, operational risks

User request:
{user_prompt}

Output format MUST be exactly a JSON array like:
[
  {{"agent":"market_intel_agent","objective":"..."}},
  {{"agent":"pricing_agent","objective":"..."}},
  {{"agent":"ops_agent","objective":"..."}}
]

Rules:
- agent must be one of ["market_intel_agent","pricing_agent","ops_agent"]
- objective must be specific and actionable (10-25 words)
"""

    resp = client.chat.completions.create(
        model=PLANNER_MODEL,
        messages=[{"role": "user", "content": planner_prompt}],
        temperature=0,
        max_tokens=300,
    )

    raw = (resp.choices[0].message.content or "").strip()

    # Parse JSON safely
    try:
        tasks = json.loads(raw)
        if not isinstance(tasks, list) or len(tasks) != 3:
            raise ValueError("Planner did not return exactly 3 tasks.")
        for t in tasks:
            if t.get("agent") not in ["market_intel_agent", "pricing_agent", "ops_agent"]:
                raise ValueError("Invalid agent in planner output.")
            if not isinstance(t.get("objective"), str) or len(t["objective"]) < 10:
                raise ValueError("Invalid objective in planner output.")
    except Exception as e:
        print(f"⚠️ Planner JSON parse/validation failed: {e}")
        print("⚠️ Falling back to default tasks.")
        tasks = [
            {"agent": "market_intel_agent", "objective": "Analyze target market demand, segments, and trends for the proposed launch."},
            {"agent": "pricing_agent", "objective": "Review competitor pricing and propose a pricing + monetization strategy."},
            {"agent": "ops_agent", "objective": "Assess operational feasibility, costs, timeline, and key execution risks."},
        ]

    # Create tasks in MongoDB
    for t in tasks:
        task_id = f"task_{uuid.uuid4().hex[:8]}"

        embedding = None
        try:
            embedding = voyage_embed(f"{t['agent']} :: {t['objective']}")
        except Exception as emb_err:
            # Don't break demo if embedding fails
            print(f"⚠️ Task embedding skipped ({task_id}): {emb_err}")

        create_task(
            task_id=task_id,
            agent_id=t["agent"],
            objective=t["objective"],
            embedding=embedding
        )

    print("✅ Planner created tasks:")
    for t in tasks:
        print(f"  - {t['agent']}: {t['objective']}")

    return tasks
