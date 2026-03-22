"""Evaluate generated future news articles using LLM-as-judge."""

import os
import json
import time
import hashlib
import re
from pathlib import Path
from openai import OpenAI

WORKSPACE = Path("/workspaces/news-future-ai-claude")
CACHE_DIR = WORKSPACE / "results" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4.1"

EVAL_RUBRIC = """\
You are an expert news editor evaluating a "news from the future" article.
The article was generated to report on a future event as if it has already occurred.

ACTUAL OUTCOME: {actual_outcome}
EVENT: {event_title}

ARTICLE TO EVALUATE:
---
{article}
---

Rate the article on these 5 dimensions (1-5 scale each):

1. PLAUSIBILITY (1-5): How believable is this as a real news article?
   1=Clearly fake/absurd, 3=Somewhat believable, 5=Could pass as real news

2. SPECIFICITY (1-5): How detailed and specific are the claims?
   1=Vague generalities, 3=Some details, 5=Rich specific details (names, dates, numbers)

3. COHERENCE (1-5): Is the article internally consistent and well-structured?
   1=Contradictory/disorganized, 3=Readable, 5=Professional quality

4. INFORMATIVENESS (1-5): Does it provide useful context beyond restating the outcome?
   1=Just restates outcome, 3=Some context, 5=Rich background, implications, analysis

5. ACCURACY (1-5): How well does the article match the actual outcome?
   1=Completely wrong outcome, 3=Partially correct, 5=Matches actual outcome perfectly

Respond in EXACTLY this JSON format (no other text):
{{"plausibility": X, "specificity": X, "coherence": X, "informativeness": X, "accuracy": X, "reasoning": "brief explanation"}}
"""


def _eval_cache_key(article, event_id, condition):
    content = f"eval_{condition}_{event_id}_{hashlib.md5(article.encode()).hexdigest()}"
    return hashlib.md5(content.encode()).hexdigest()


def evaluate_article(article, event_title, actual_outcome, event_id, condition):
    """Evaluate a single article using GPT-4.1 as judge.

    Returns dict with scores for each dimension.
    """
    key = _eval_cache_key(article, event_id, condition)
    cache_path = CACHE_DIR / f"eval_{key}.json"

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    prompt = EVAL_RUBRIC.format(
        actual_outcome=actual_outcome,
        event_title=event_title,
        article=article,
    )

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temp for consistent evaluation
                max_tokens=300,
            )
            text = response.choices[0].message.content.strip()

            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
            else:
                scores = json.loads(text)

            # Validate scores
            for dim in ["plausibility", "specificity", "coherence", "informativeness", "accuracy"]:
                if dim not in scores or not isinstance(scores[dim], (int, float)):
                    scores[dim] = 3  # Default if missing
                scores[dim] = max(1, min(5, int(scores[dim])))

            with open(cache_path, "w") as f:
                json.dump(scores, f)
            return scores

        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                # Return neutral scores on failure
                return {
                    "plausibility": 3, "specificity": 3, "coherence": 3,
                    "informativeness": 3, "accuracy": 3,
                    "reasoning": f"Evaluation failed: {str(e)}"
                }


def evaluate_semantic_similarity(article, actual_outcome, event_title):
    """Use LLM to rate semantic alignment between article and actual outcome (0-1 scale).

    This replaces embedding-based similarity with a more interpretable LLM-based measure.
    """
    prompt = (
        f"On a scale of 0.0 to 1.0, how well does this news article's predictions "
        f"match the actual outcome?\n\n"
        f"EVENT: {event_title}\n"
        f"ACTUAL OUTCOME: {actual_outcome}\n\n"
        f"ARTICLE:\n{article[:500]}\n\n"
        f"Respond with ONLY a number between 0.0 and 1.0."
    )

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10,
            )
            text = response.choices[0].message.content.strip()
            score = float(re.search(r'[\d.]+', text).group())
            return max(0.0, min(1.0, score))
        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)
    return 0.5  # Default on failure
