from agents.market_agent import run as market_run
from agents.pricing_agent import run as pricing_run
from agents.ops_agent import run as ops_run

def run_all_agents():
    market_run()
    pricing_run()
    ops_run()