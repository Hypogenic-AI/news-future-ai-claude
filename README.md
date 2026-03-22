# News from the Future

**AI-generated news articles powered by prediction markets and LLMs.**

This research project builds and evaluates an end-to-end system that combines large language models (GPT-4.1) with prediction market data (Polymarket) to generate plausible news articles about future events.

## Key Findings

- **Market data is essential for accuracy**: Without market conditioning, GPT-4.1 produces well-written articles about the *wrong* future (accuracy 1.72/5). With market data, accuracy jumps to 4.64-4.88/5 (p < 0.0001, Cohen's d > 2.0).
- **Writing quality is uniformly high**: All conditions produce professional-quality articles (coherence 5.0/5, plausibility ~4.9/5). The challenge is *what to write*, not *how to write*.
- **Different strategies serve different purposes**: Direct conditioning maximizes accuracy; Superforecaster persona maximizes informativeness; MCP provides the best balance.
- **A functional web app demonstrates the system** with live Polymarket data.

## Quick Start

```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install openai requests numpy scipy matplotlib seaborn pandas scikit-learn flask

# Set API key
export OPENAI_API_KEY=your_key_here

# Run experiments
python src/run_experiment.py

# Run analysis
python src/analyze_results.py

# Launch web app
python src/webapp.py
# Visit http://localhost:5000
```

## Project Structure

```
├── REPORT.md                    # Full research report with results
├── planning.md                  # Research plan and methodology
├── src/
│   ├── data_loader.py           # Load Polymarket prediction market data
│   ├── article_generator.py     # Generate articles under 4 conditions
│   ├── evaluator.py             # LLM-as-judge evaluation
│   ├── run_experiment.py        # Main experiment runner
│   ├── analyze_results.py       # Statistical analysis & visualizations
│   └── webapp.py                # Flask web application
├── results/
│   ├── experiment_results.json  # Raw evaluation scores
│   ├── articles/                # Generated articles
│   ├── plots/                   # Visualization outputs
│   ├── descriptive_stats.csv    # Summary statistics
│   └── statistical_tests.csv    # Statistical test results
├── datasets/                    # Prediction market data
├── papers/                      # Related research papers
├── code/                        # Reference implementations
└── literature_review.md         # Literature review
```

## Methodology

1. **Data**: 25 resolved Polymarket events (top by trading volume, $12.6B total)
2. **Generation**: GPT-4.1 generates articles under 4 conditions (no market, direct, MCP, superforecaster)
3. **Evaluation**: LLM-as-judge scores on 5 dimensions + semantic similarity
4. **Analysis**: Wilcoxon signed-rank tests, Cohen's d effect sizes, Bonferroni correction

See [REPORT.md](REPORT.md) for full details.

## Web Application

The Flask web app (`src/webapp.py`) fetches live prediction markets from Polymarket and generates future news articles on demand using GPT-4.1 with Market-Conditioned Prompting.

## License

Research project for academic purposes.
