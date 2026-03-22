"""Main experiment runner: generate articles and evaluate them across all conditions."""

import json
import sys
import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/workspaces/news-future-ai-claude")
sys.path.insert(0, str(WORKSPACE / "src"))

from data_loader import load_polymarket_events, prepare_experiment_data
from article_generator import generate_all_conditions, GENERATORS
from evaluator import evaluate_article, evaluate_semantic_similarity

# Reproducibility
random.seed(42)
np.random.seed(42)

N_EVENTS = 25  # Number of events to test


def run_experiment():
    """Run the full experiment across all events and conditions."""
    print(f"[{datetime.now():%H:%M:%S}] Loading data...")
    events = load_polymarket_events(max_events=N_EVENTS)
    tasks = prepare_experiment_data(events)
    print(f"  Loaded {len(tasks)} events for experiment")

    results = []
    all_articles = {}

    for i, task in enumerate(tasks):
        print(f"\n[{datetime.now():%H:%M:%S}] Event {i+1}/{len(tasks)}: {task['title'][:60]}")

        # Generate articles for all conditions
        articles = generate_all_conditions(task)
        all_articles[task["event_id"]] = {
            "title": task["title"],
            "winning_outcome": task["winning_outcome"],
            "articles": articles,
        }

        # Evaluate each article
        for condition, article in articles.items():
            print(f"  Evaluating {condition}...", end=" ", flush=True)

            scores = evaluate_article(
                article=article,
                event_title=task["title"],
                actual_outcome=task["winning_outcome"],
                event_id=task["event_id"],
                condition=condition,
            )

            # Semantic similarity for market-conditioned articles
            sim_score = evaluate_semantic_similarity(
                article=article,
                actual_outcome=task["winning_outcome"],
                event_title=task["title"],
            )

            result = {
                "event_id": task["event_id"],
                "event_title": task["title"],
                "condition": condition,
                "winning_outcome": task["winning_outcome"],
                "volume": task["volume"],
                **{k: v for k, v in scores.items() if k != "reasoning"},
                "semantic_similarity": sim_score,
                "reasoning": scores.get("reasoning", ""),
            }
            results.append(result)
            print(f"P={scores['plausibility']} S={scores['specificity']} "
                  f"C={scores['coherence']} I={scores['informativeness']} "
                  f"A={scores['accuracy']} Sim={sim_score:.2f}")

        # Small delay between events to avoid rate limits
        time.sleep(0.5)

    # Save results
    results_path = WORKSPACE / "results" / "experiment_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[{datetime.now():%H:%M:%S}] Results saved to {results_path}")

    # Save articles
    articles_path = WORKSPACE / "results" / "articles" / "all_articles.json"
    with open(articles_path, "w") as f:
        json.dump(all_articles, f, indent=2)
    print(f"Articles saved to {articles_path}")

    # Save experiment config
    config = {
        "model": "gpt-4.1",
        "n_events": N_EVENTS,
        "conditions": list(GENERATORS.keys()),
        "seed": 42,
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
    }
    config_path = WORKSPACE / "results" / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    return results


def print_summary(results):
    """Print a quick summary table of results."""
    import numpy as np

    conditions = sorted(set(r["condition"] for r in results))
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy", "semantic_similarity"]

    print(f"\n{'='*80}")
    print(f"EXPERIMENT SUMMARY ({len(results)} evaluations across {len(conditions)} conditions)")
    print(f"{'='*80}")

    header = f"{'Condition':<20}" + "".join(f"{m[:6]:>10}" for m in metrics)
    print(header)
    print("-" * len(header))

    for cond in conditions:
        cond_results = [r for r in results if r["condition"] == cond]
        row = f"{cond:<20}"
        for metric in metrics:
            vals = [r[metric] for r in cond_results]
            mean = np.mean(vals)
            std = np.std(vals)
            row += f"{mean:>7.2f}±{std:.1f}"
        print(row)


if __name__ == "__main__":
    results = run_experiment()
    print_summary(results)
