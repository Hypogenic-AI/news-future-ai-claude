# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project "News from the Future: Combining LLMs with Prediction Markets to Generate Plausible News Articles About Future Events."

## Papers
Total papers downloaded: 13

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Leveraging Log Probabilities for Forecasting | Multiple | 2025 | papers/2501.04880_*.pdf | Novel forecast generation + log-prob calibration |
| Outcome-Driven Fine-Tuning (Polymarket) | Multiple | 2025 | papers/2502.05253_*.pdf | Self-play DPO with Polymarket data |
| Mention Markets: Context Design | Multiple | 2026 | papers/2602.21229_*.pdf | Market-Conditioned Prompting, MixMCP |
| Time-R1: Temporal Reasoning | UIUC | 2025 | papers/2505.13508_*.pdf | Future headline generation, 3B model |
| ForecastBench | Karger et al. | 2024 | papers/2409.19839_*.pdf | Dynamic benchmark, ICLR 2025 |
| AIA Forecaster | Bridgewater | 2025 | papers/2511.07678_*.pdf | Multi-agent, superforecaster-level |
| PROPHET Benchmark | Multiple | 2025 | papers/2504.01509_*.pdf | CIL evidence validation |
| KalshiBench | Nel | 2025 | papers/2512.16030_*.pdf | Calibration benchmark, 1531 questions |
| Fake Prediction Markets | Todasco | 2025 | papers/2512.05998_*.pdf | Confidence via financial framing |
| AI-Augmented Predictions | Schoenegger et al. | 2024 | papers/2402.07862_*.pdf | Human+LLM forecasting, +41% accuracy |
| LLMs vs Expert Forecasters | Lu | 2025 | papers/2507.04562_*.pdf | Narrative prompt decreases accuracy |
| Prompt Engineering Forecasting | Multiple | 2025 | papers/2506.01578_*.pdf | Systematic prompt comparison |
| News to Forecast (NeurIPS) | Multiple | 2024 | papers/2409.17515_*.pdf | Event-driven time series forecasting |

See papers/README.md for detailed descriptions.

## Datasets
Total datasets downloaded: 4

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| KalshiBench | HuggingFace | 1,531 questions | Calibration eval | datasets/kalshibench/ | CFTC-regulated Kalshi exchange |
| ForecastBench | GitHub | 500 questions/set | Forecasting | datasets/forecastbench/ | Updated nightly, CC BY-SA 4.0 |
| Polymarket Events | Gamma API | 100 top resolved | Forecasting | datasets/polymarket/ | Expandable via API |
| Metaculus (via ForecastBench) | ForecastBench | Included | Forecasting | code/forecastbench-datasets/ | Auth required for direct API |

See datasets/README.md for detailed descriptions and download instructions.

## Code Repositories
Total repositories cloned: 7

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| ForecastBench | github.com/forecastingresearch/forecastbench | Benchmark code | code/forecastbench/ | ICLR 2025 |
| ForecastBench Datasets | github.com/forecastingresearch/forecastbench-datasets | Question sets | code/forecastbench-datasets/ | Updated nightly |
| Polymarket Agents | github.com/Polymarket/agents | AI trading framework | code/polymarket-agents/ | MIT license |
| Time-R1 | github.com/ulab-uiuc/Time-R1 | Temporal reasoning | code/time-r1/ | HF models available |
| PROPHET | github.com/TZWwww/PROPHET | Evidence validation | code/prophet/ | CIL metric |
| Metaculus Tools | github.com/Metaculus/forecasting-tools | Forecasting bot framework | code/metaculus-forecasting-tools/ | Official API wrapper |
| Prediction Market Analysis | github.com/Jon-Becker/prediction-market-analysis | Market data collection | code/prediction-market-analysis/ | Largest public PM dataset |

See code/README.md for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
1. Searched arXiv, Semantic Scholar, and Papers with Code for papers at the intersection of LLMs, prediction markets, and forecasting
2. Focused on 2024-2026 papers with priority on those with code/datasets
3. Used multiple query variations: "prediction markets LLM", "LLM forecasting", "news generation future events", "superforecasting calibration"
4. Searched HuggingFace, GitHub, and Kaggle for datasets
5. Identified key code repositories from paper references and platform official repos

### Selection Criteria
- Papers directly combining LLMs with prediction markets or forecasting
- Papers on temporal reasoning and future text generation
- Benchmarks with publicly available datasets
- Code repositories enabling data access and baseline implementations

### Challenges Encountered
- Metaculus API requires authentication (worked around via ForecastBench)
- Paper-finder service not available (used web search + arXiv direct download)
- No existing paper directly generates full news articles from prediction market data — this is the research gap

### Gaps and Workarounds
- **News generation evaluation**: No standard benchmark exists for evaluating plausibility of generated future news. Recommend adapting AvgMaxSim from Time-R1 + human evaluation.
- **Large-scale Polymarket data**: Full historical dataset available via prediction-market-analysis repo (requires downloading tar archive from Cloudflare R2).
- **NYT articles**: Time-R1's training data (200K+ NYT articles) not directly available but Time-R1 models are on HuggingFace.

## Recommendations for Experiment Design

1. **Primary dataset(s)**: ForecastBench (diverse, continuously updated, standard benchmark) + KalshiBench (calibration focus, ground truth from regulated exchange) + Polymarket resolved events (for training signal)

2. **Baseline methods**:
   - Vanilla LLM generation (no market data)
   - Market-only baseline (report consensus probability)
   - RAG-only (news retrieval without market signal)
   - Market-Conditioned Prompting (MCP from Mention Markets paper)
   - Time-R1 temporal generation approach

3. **Evaluation metrics**:
   - Brier Score (probability calibration)
   - AvgMaxSim (semantic similarity to real outcomes)
   - ECE (calibration error)
   - Human evaluation (plausibility, coherence, informativeness)

4. **Code to adapt/reuse**:
   - Polymarket Agents (market data access)
   - ForecastBench (benchmark infrastructure and scoring)
   - PROPHET (evidence validation via CIL)
   - Time-R1 (temporal reasoning and evaluation)
   - Metaculus Forecasting Tools (question access)
