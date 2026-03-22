"""Flask web application: News from the Future.

Fetches live prediction market data and generates future news articles using LLMs.
"""

import os
import json
import time
import requests
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
MODEL = "gpt-4.1"

WORKSPACE = Path("/workspaces/news-future-ai-claude")

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News from the Future</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #f5f0e8;
            color: #2c2c2c;
            line-height: 1.6;
        }
        header {
            background: #1a1a2e;
            color: #e8d5b5;
            text-align: center;
            padding: 2rem 1rem;
            border-bottom: 4px solid #c4a35a;
        }
        header h1 {
            font-size: 2.5rem;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        header p {
            font-style: italic;
            margin-top: 0.5rem;
            color: #a89070;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 1rem; }
        .market-list {
            display: grid;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .market-card {
            background: white;
            border: 1px solid #d4c5a0;
            border-radius: 4px;
            padding: 1.2rem;
            cursor: pointer;
            transition: box-shadow 0.2s, transform 0.1s;
        }
        .market-card:hover {
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            transform: translateY(-1px);
        }
        .market-card h3 {
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #1a1a2e;
        }
        .market-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.85rem;
            color: #666;
        }
        .prob-badge {
            background: #1a1a2e;
            color: #c4a35a;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: bold;
        }
        .article-view {
            background: white;
            border: 1px solid #d4c5a0;
            border-radius: 4px;
            padding: 2rem;
            margin-top: 1.5rem;
        }
        .article-view h2 {
            font-size: 1.6rem;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid #c4a35a;
            padding-bottom: 0.5rem;
        }
        .article-dateline {
            font-style: italic;
            color: #888;
            margin-bottom: 1rem;
        }
        .article-body { white-space: pre-wrap; line-height: 1.8; }
        .loading {
            text-align: center;
            padding: 2rem;
            color: #888;
            font-style: italic;
        }
        .back-btn {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            background: #1a1a2e;
            color: #c4a35a;
            text-decoration: none;
            border-radius: 3px;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .disclaimer {
            text-align: center;
            font-size: 0.8rem;
            color: #999;
            padding: 1rem;
            margin-top: 2rem;
            border-top: 1px solid #d4c5a0;
        }
        #markets-container { min-height: 200px; }
    </style>
</head>
<body>
    <header>
        <h1>News from the Future</h1>
        <p>AI-generated news articles powered by prediction markets &amp; GPT-4.1</p>
    </header>
    <div class="container">
        <div id="app">
            <div id="markets-container">
                <p class="loading">Loading prediction markets...</p>
            </div>
        </div>
        <div class="disclaimer">
            This is a research prototype. Articles are AI-generated fiction based on
            prediction market probabilities. Not real news. Not financial advice.
        </div>
    </div>
    <script>
        async function loadMarkets() {
            const container = document.getElementById('markets-container');
            try {
                const resp = await fetch('/api/markets');
                const markets = await resp.json();
                let html = '<div class="market-list">';
                for (const m of markets) {
                    const prob = Math.round(m.probability * 100);
                    html += `
                        <div class="market-card" onclick="generateArticle('${m.id}', '${m.question.replace(/'/g, "\\\\'")}')">
                            <h3>${m.question}</h3>
                            <div class="market-meta">
                                <span class="prob-badge">${prob}% likely</span>
                                <span>Ends: ${m.end_date || 'TBD'}</span>
                            </div>
                        </div>`;
                }
                html += '</div>';
                container.innerHTML = html;
            } catch(e) {
                container.innerHTML = '<p class="loading">Error loading markets. Showing demo data...</p>';
                loadDemoMarkets(container);
            }
        }

        function loadDemoMarkets(container) {
            const demos = [
                {id: 'demo1', question: 'Will AI surpass human performance on all benchmarks by 2027?', probability: 0.35},
                {id: 'demo2', question: 'Will SpaceX land humans on Mars before 2030?', probability: 0.12},
                {id: 'demo3', question: 'Will global temperatures exceed 1.5C above pre-industrial levels in 2026?', probability: 0.65},
            ];
            let html = '<div class="market-list">';
            for (const m of demos) {
                html += `
                    <div class="market-card" onclick="generateArticle('${m.id}', '${m.question}')">
                        <h3>${m.question}</h3>
                        <div class="market-meta"><span class="prob-badge">${Math.round(m.probability*100)}% likely</span></div>
                    </div>`;
            }
            html += '</div>';
            container.innerHTML = html;
        }

        async function generateArticle(marketId, question) {
            const container = document.getElementById('markets-container');
            container.innerHTML = `
                <button class="back-btn" onclick="loadMarkets()">&#8592; Back to markets</button>
                <div class="article-view">
                    <h2>${question}</h2>
                    <p class="loading">Generating news from the future...</p>
                </div>`;
            try {
                const resp = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({market_id: marketId, question: question})
                });
                const data = await resp.json();
                container.innerHTML = `
                    <button class="back-btn" onclick="loadMarkets()">&#8592; Back to markets</button>
                    <div class="article-view">
                        <h2>${data.headline}</h2>
                        <p class="article-dateline">${data.dateline}</p>
                        <div class="article-body">${data.article}</div>
                    </div>`;
            } catch(e) {
                container.innerHTML = `
                    <button class="back-btn" onclick="loadMarkets()">&#8592; Back to markets</button>
                    <div class="article-view"><p>Error generating article. Please try again.</p></div>`;
            }
        }

        loadMarkets();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/markets")
def api_markets():
    """Fetch active prediction markets from Polymarket."""
    try:
        url = "https://gamma-api.polymarket.com/events?active=true&limit=20&order=volume&ascending=false"
        resp = requests.get(url, timeout=10)
        events = resp.json()

        markets = []
        for ev in events:
            for m in ev.get("markets", [])[:1]:  # Take first market per event
                try:
                    prices = json.loads(m.get("outcomePrices", "[]"))
                    prob = float(prices[0]) if prices else 0.5
                except (json.JSONDecodeError, IndexError, ValueError):
                    prob = 0.5

                markets.append({
                    "id": m.get("id", ""),
                    "question": m.get("question", ev.get("title", "")),
                    "probability": prob,
                    "end_date": (m.get("endDate") or "")[:10],
                })

        return jsonify(markets[:15])
    except Exception:
        return jsonify([])


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """Generate a future news article for a given market question."""
    data = request.json
    question = data.get("question", "")

    system = (
        "You are an expert news analyst who combines prediction market signals "
        "with contextual analysis to produce compelling future news reporting.\n\n"
        "Write a news article FROM THE FUTURE, as if this event has already occurred. "
        "The article should be 200-300 words, written in professional news style with:\n"
        "- A compelling headline\n"
        "- A dateline (city, future date)\n"
        "- Specific details, quotes from relevant figures, and context\n"
        "- Discussion of implications and what comes next\n\n"
        "Format your response as JSON with keys: headline, dateline, article"
    )

    user = f"Write a future news article about: {question}"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.8,
            max_tokens=600,
        )
        text = response.choices[0].message.content

        # Try to parse JSON response
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {
                "headline": question,
                "dateline": "The Future",
                "article": text,
            }

        return jsonify(result)
    except Exception as e:
        return jsonify({
            "headline": question,
            "dateline": "The Future",
            "article": f"[Article generation temporarily unavailable: {str(e)}]",
        })


if __name__ == "__main__":
    print("Starting News from the Future web app...")
    print("Visit http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
