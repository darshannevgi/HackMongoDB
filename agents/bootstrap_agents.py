from db.agent_registry import register_agent

def bootstrap_agents():
    register_agent(
        agent_id="market_intel_agent",
        role="Market Intelligence",
        description="Analyzes market demand, customer personas, and regional trends",
        skills=["market sizing", "customer research", "trend analysis"]
    )

    register_agent(
        agent_id="pricing_agent",
        role="Pricing Strategy",
        description="Optimizes pricing, monetization, and revenue models",
        skills=["pricing strategy", "revenue modeling"]
    )

    register_agent(
        agent_id="ops_agent",
        role="Feasibility & Operations",
        description="Evaluates scalability, costs, and operational risks",
        skills=["cost analysis", "scalability", "risk assessment"]
    )

    print("✅ Agents registered successfully")
