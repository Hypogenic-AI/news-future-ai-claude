"""Load and prepare prediction market data for news generation experiments."""

import json
import random
from pathlib import Path

WORKSPACE = Path("/workspaces/news-future-ai-claude")


def load_polymarket_events(max_events=30):
    """Load resolved Polymarket events with sufficient detail for news generation.

    Returns a list of dicts with: title, description, winning outcome, market details.
    """
    path = WORKSPACE / "datasets" / "polymarket" / "top_resolved_events.json"
    with open(path) as f:
        raw = json.load(f)

    events = []
    for ev in raw:
        title = ev.get("title", "")
        description = ev.get("description", "")
        markets = ev.get("markets", [])
        if not title or not markets:
            continue

        # Find winning outcome(s) by checking outcomePrices
        winners = []
        all_markets = []
        for m in markets:
            question = m.get("question", "")
            try:
                prices = json.loads(m.get("outcomePrices", "[]"))
            except (json.JSONDecodeError, TypeError):
                prices = []

            resolved_yes = prices and float(prices[0]) > 0.5
            item_title = m.get("groupItemTitle", "")

            all_markets.append({
                "question": question,
                "resolved_yes": resolved_yes,
                "group_item_title": item_title,
                "outcome_prices": prices,
            })

            if resolved_yes and item_title:
                winners.append(item_title)

        # Build winning outcome description
        if winners:
            winning_outcome = ", ".join(winners)
        else:
            # For single-market events, use the question itself
            for mk in all_markets:
                if mk["resolved_yes"]:
                    winning_outcome = mk["question"].replace("Will ", "").rstrip("?")
                    break
            else:
                winning_outcome = "Event resolved (details unclear)"

        events.append({
            "id": ev.get("id", ""),
            "title": title,
            "description": description,
            "end_date": ev.get("endDate", ""),
            "volume": ev.get("volume", 0),
            "winning_outcome": winning_outcome,
            "markets": all_markets,
            "num_markets": len(all_markets),
        })

    events.sort(key=lambda x: x["volume"], reverse=True)
    return events[:max_events]


def prepare_experiment_data(events, seed=42):
    """Prepare events for the experiment.

    Returns list of task dicts ready for article generation.
    """
    random.seed(seed)

    tasks = []
    for ev in events:
        # Build market context string (top outcomes)
        market_lines = []
        for m in ev["markets"][:10]:  # Cap at 10 for prompt length
            status = "YES" if m["resolved_yes"] else "NO"
            label = m["group_item_title"] or m["question"][:60]
            market_lines.append(f"  - {label}: Resolved {status}")

        tasks.append({
            "event_id": ev["id"],
            "title": ev["title"],
            "description": ev["description"],
            "end_date": ev["end_date"],
            "volume": ev["volume"],
            "winning_outcome": ev["winning_outcome"],
            "market_context": "\n".join(market_lines),
            "num_markets": ev["num_markets"],
        })

    return tasks


if __name__ == "__main__":
    events = load_polymarket_events(max_events=30)
    print(f"Loaded {len(events)} Polymarket events")
    for ev in events[:5]:
        print(f"\n  {ev['title']} (volume: ${ev['volume']:,.0f})")
        print(f"  Winner: {ev['winning_outcome']}")
        print(f"  Markets: {ev['num_markets']}")
