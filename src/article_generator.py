"""Generate future news articles using different conditioning strategies."""

import os
import json
import time
import hashlib
from pathlib import Path
from openai import OpenAI

WORKSPACE = Path("/workspaces/news-future-ai-claude")
CACHE_DIR = WORKSPACE / "results" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4.1"


def _cache_key(prompt_system, prompt_user, condition):
    """Generate a deterministic cache key."""
    content = f"{condition}|{prompt_system}|{prompt_user}"
    return hashlib.md5(content.encode()).hexdigest()


def _cached_call(prompt_system, prompt_user, condition, temperature=0.7):
    """Call OpenAI API with caching to avoid redundant calls."""
    key = _cache_key(prompt_system, prompt_user, condition)
    cache_path = CACHE_DIR / f"{key}.json"

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)["content"]

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user},
                ],
                temperature=temperature,
                max_tokens=800,
            )
            content = response.choices[0].message.content
            with open(cache_path, "w") as f:
                json.dump({"condition": condition, "content": content}, f)
            return content
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise e


# ── Condition 1: No Market Data (Baseline) ──────────────────────────────────

def generate_no_market(task):
    """Generate future news with only the event title — no market data."""
    system = (
        "You are a news journalist writing a plausible future news article. "
        "Write a short article (150-250 words) predicting the most likely outcome "
        "of the following event. Write as if reporting from the future, after the "
        "event has occurred. Include specific details, quotes, and context."
    )
    user = (
        f"Write a future news article about: {task['title']}\n\n"
        f"Context: {task['description'][:300]}\n"
        f"Expected resolution date: {task['end_date'][:10]}"
    )
    return _cached_call(system, user, f"no_market_{task['event_id']}")


# ── Condition 2: Direct Market Conditioning ──────────────────────────────────

def generate_direct_market(task):
    """Generate future news with market data included directly in prompt."""
    system = (
        "You are a news journalist writing a plausible future news article. "
        "You have access to prediction market data showing the resolved outcomes. "
        "Write a short article (150-250 words) as if reporting from the future, "
        "after the event has occurred. Base your article on the market outcomes. "
        "Include specific details, quotes, and context."
    )
    user = (
        f"Write a future news article about: {task['title']}\n\n"
        f"Context: {task['description'][:300]}\n"
        f"Expected resolution date: {task['end_date'][:10]}\n\n"
        f"Prediction market outcome: {task['winning_outcome']}\n\n"
        f"Market details:\n{task['market_context']}"
    )
    return _cached_call(system, user, f"direct_market_{task['event_id']}")


# ── Condition 3: Market-Conditioned Prompting (MCP) ──────────────────────────

def generate_mcp(task):
    """Generate future news using Market-Conditioned Prompting framework.

    Inspired by the MCP approach from the Mention Markets paper:
    treat market probability as a Bayesian prior and update with textual evidence.
    """
    system = (
        "You are an expert news analyst who combines prediction market signals "
        "with contextual analysis to produce accurate future reporting.\n\n"
        "METHODOLOGY:\n"
        "1. Start with the prediction market outcome as your primary signal\n"
        "2. Consider what supporting evidence and context would exist\n"
        "3. Reason about the causal chain: what events led to this outcome?\n"
        "4. Generate a news article that tells the story coherently\n\n"
        "Write a short article (150-250 words) from the future, after the event "
        "has resolved. Include the causal narrative, key moments, and implications."
    )
    user = (
        f"EVENT: {task['title']}\n"
        f"BACKGROUND: {task['description'][:300]}\n"
        f"RESOLUTION DATE: {task['end_date'][:10]}\n\n"
        f"MARKET SIGNAL (high confidence): The outcome was: {task['winning_outcome']}\n\n"
        f"DETAILED MARKET RESOLUTION:\n{task['market_context']}\n\n"
        "Using the market signal as your anchor, write a compelling news article "
        "that explains HOW and WHY this outcome occurred. Include plausible details "
        "about the key moments, reactions, and implications."
    )
    return _cached_call(system, user, f"mcp_{task['event_id']}")


# ── Condition 4: Superforecaster Persona ─────────────────────────────────────

def generate_superforecaster(task):
    """Generate future news using superforecaster reasoning + market data."""
    system = (
        "You are a superforecaster (in the tradition of Philip Tetlock's research) "
        "who also writes news articles. You combine rigorous probabilistic thinking "
        "with compelling narrative.\n\n"
        "YOUR APPROACH:\n"
        "- Consider base rates and reference classes\n"
        "- Weigh multiple information sources\n"
        "- Acknowledge uncertainty where appropriate\n"
        "- Use prediction market data as strong but not infallible signal\n"
        "- Provide nuanced analysis, not just outcomes\n\n"
        "Write a short article (150-250 words) from the future. Include calibrated "
        "language reflecting your confidence level. Note any surprising aspects "
        "or what the outcome tells us about the broader landscape."
    )
    user = (
        f"EVENT: {task['title']}\n"
        f"BACKGROUND: {task['description'][:300]}\n"
        f"RESOLUTION DATE: {task['end_date'][:10]}\n\n"
        f"PREDICTION MARKET OUTCOME: {task['winning_outcome']}\n"
        f"MARKET DETAILS:\n{task['market_context']}\n\n"
        "Write a future news article incorporating superforecaster-style analysis. "
        "Discuss what made this outcome likely or surprising, and what it signals."
    )
    return _cached_call(system, user, f"superforecaster_{task['event_id']}")


# ── Dispatcher ───────────────────────────────────────────────────────────────

GENERATORS = {
    "no_market": generate_no_market,
    "direct_market": generate_direct_market,
    "mcp": generate_mcp,
    "superforecaster": generate_superforecaster,
}


def generate_all_conditions(task):
    """Generate articles for all 4 conditions for a single task."""
    results = {}
    for name, gen_fn in GENERATORS.items():
        results[name] = gen_fn(task)
    return results


if __name__ == "__main__":
    from data_loader import load_polymarket_events, prepare_experiment_data

    events = load_polymarket_events(max_events=3)
    tasks = prepare_experiment_data(events)

    for task in tasks[:1]:
        print(f"\n{'='*60}")
        print(f"Event: {task['title']}")
        print(f"Outcome: {task['winning_outcome']}")
        articles = generate_all_conditions(task)
        for cond, article in articles.items():
            print(f"\n--- {cond} ---")
            print(article[:200] + "...")
