import os
from db.shared_context import retrieve_context, write_context
from openai import OpenAI

AGENT_ID = "launch_lead"

# Initialize Fireworks-compatible OpenAI client
fireworks = OpenAI(
    api_key="fw_2vKeHWeZyu99qXudDFe9ww",
    base_url="https://api.fireworks.ai/inference/v1"
)

def run():
    print("🚀 Launch Lead Agent is running...")

    insights = retrieve_context(
        query="product launch",
        limit=10
    )

    context_block = "\n".join(f"- {item['content']}" for item in insights)

    prompt = f"""
You are the launch lead agent.
Synthesize the following expert insights into a final launch recommendation:

{context_block}

Provide:
1. Go / No-Go decision
2. Target customer
3. Pricing strategy
4. Key risks
"""

    # Fireworks AI call
    result = fireworks.chat.completions.create(
        model="accounts/fireworks/models/deepseek-r1-0528",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    final_output = result.choices[0].message.content

    write_context(
        task_id="final_decision",
        agent_id=AGENT_ID,
        content=final_output
    )

    print("🎯 Final synthesis complete:")
    print(final_output)
