# Literature Review: News from the Future

## Research Area Overview

This review covers the intersection of **large language models (LLMs)** and **prediction markets** for generating plausible news articles about future events. The field spans three active research areas: (1) LLM-based forecasting and calibration, (2) prediction market data as training/evaluation signals, and (3) temporal reasoning and future text generation. Research has accelerated dramatically in 2024-2026, with LLMs approaching but not yet matching expert human forecasters (superforecasters).

---

## Key Papers

### 1. Leveraging Log Probabilities in Language Models to Forecast Future Events
- **Authors**: Multiple (ICSC 2025)
- **Year**: 2025
- **arXiv**: 2501.04880
- **Key Contribution**: First system to generate novel "blue-sky" future event forecasts (not just estimate probabilities of known events) and assign calibrated probabilities using log probabilities.
- **Methodology**: Three-component pipeline: Forecast Generator (trend extraction from ~45K articles), Probability Estimator (weighted log-prob aggregation across all token completions), Fact Checker. Uses SVR for post-hoc calibration.
- **Datasets**: 150 forecasts across 15 topics, 240-day gap between prediction and fact-checking.
- **Results**: Brier score 0.186 (+26% over random, +19% over vanilla GPT-4o). Competitive with prediction market baselines (~0.182 Manifold).
- **Relevance**: **Directly applicable** — demonstrates full pipeline from trend analysis → forecast generation → probability estimation → fact checking. Core architecture for a "futures news" system.

### 2. LLMs Can Teach Themselves to Better Predict the Future (Outcome-Driven Fine-Tuning)
- **Authors**: Multiple
- **Year**: 2025
- **arXiv**: 2502.05253
- **Key Contribution**: Outcome-driven fine-tuning framework using Polymarket data. Models generate reasoning traces via self-play, ranked by proximity to actual outcomes, then fine-tuned with DPO.
- **Methodology**: 6-step pipeline: data collection from Polymarket → news retrieval (NewsCatcher) → self-play reasoning generation → resolution-driven re-ranking → DPO fine-tuning → evaluation.
- **Datasets**: 12,100 binary questions from Polymarket (9,800 train, 2,300 test). NewsCatcher for news context.
- **Results**: Phi-4 14B improved 7% (Brier 0.200), DeepSeek-R1 14B improved 7-10% (Brier 0.197). Both reach GPT-4o parity (0.196).
- **Relevance**: **High** — demonstrates using prediction markets as training signal. Self-play reasoning traces could serve as templates for news narrative generation.

### 3. Forecasting Future Language: Context Design for Mention Markets
- **Authors**: Multiple
- **Year**: 2026
- **arXiv**: 2602.21229
- **Key Contribution**: Shows LLMs and prediction markets are complementary. Market-Conditioned Prompting (MCP) treats market probability as a Bayesian prior that LLMs update with textual evidence.
- **Methodology**: MCP prompting with GPT-5.1. Evaluated on Kalshi earnings-call mention markets. MixMCP combines market + LLM signals (α=0.7 market weight).
- **Datasets**: 856 contracts from Kalshi, 50 companies, 70 earnings events. Prior transcripts + news articles as context.
- **Results**: MixMCP achieves best Brier score (0.1392) and accuracy (80.3%), beating either market or LLM alone. MCP excels in mid-confidence regimes (50-70%).
- **Relevance**: **Very high** — directly demonstrates market-LLM synergy. MCP framework is ideal for generating market-informed future news narratives.

### 4. Time-R1: Towards Comprehensive Temporal Reasoning
- **Authors**: UIUC
- **Year**: 2025
- **arXiv**: 2505.13508
- **Key Contribution**: Progressive RL curriculum (3 stages) that trains a 3B model to match/exceed 671B models on temporal tasks including future news headline generation.
- **Methodology**: GRPO with dynamic rule-based rewards. Stage 1: temporal comprehension (200K+ NYT articles). Stage 2: future event prediction. Stage 3: creative scenario generation (zero-shot).
- **Datasets**: NYT articles 2016-2025, Time-Bench (200K+ examples).
- **Results**: 3B model achieves 48.90% AvgMaxSim (semantic similarity to real events), outperforming 671B models. 171.6% improvement over base model.
- **Code**: https://github.com/ulab-uiuc/Time-R1
- **Relevance**: **Critical** — directly generates future news headlines with temporal grounding. AvgMaxSim metric measures plausibility of generated scenarios. Small model achieves frontier performance.

### 5. ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities
- **Authors**: Karger et al. (ICLR 2025)
- **Year**: 2024
- **arXiv**: 2409.19839
- **Key Contribution**: Dynamic, contamination-free benchmark with 1,000 questions from 9 sources (including Polymarket, Metaculus, Manifold). Updated nightly.
- **Methodology**: Automated question generation from prediction markets + real-world datasets. Questions about future events only. Includes combination questions testing covariance reasoning.
- **Datasets**: 6,435 questions from markets (2,060) and datasets (4,375). Human evaluation subset (N=200).
- **Results**: Superforecasters (0.096) > General public (0.121) ≈ Best LLM Claude-3.5-Sonnet (0.122). LLMs struggle with combination questions.
- **Code**: https://github.com/forecastingresearch/forecastbench
- **Relevance**: **High** — provides benchmark infrastructure and dataset. Reveals LLM weaknesses (covariance reasoning) important for multi-event news narratives.

### 6. AIA Forecaster: Technical Report
- **Authors**: Bridgewater AIA Labs
- **Year**: 2025
- **arXiv**: 2511.07678
- **Key Contribution**: Multi-agent LLM system achieving superforecaster-level performance. Introduces agentic search, supervisor reconciliation, and Platt scaling calibration.
- **Methodology**: M independent agents with agentic search → supervisor identifies disagreements → additional search → calibration via Platt scaling (corrects RLHF hedging bias).
- **Datasets**: ForecastBench, MarketLiquid (1,610 questions from liquid prediction markets), MarketNightly (live).
- **Results**: Matches human superforecasters on ForecastBench. Ensemble with market consensus outperforms either alone.
- **Relevance**: **High** — provides architectural blueprint for multi-agent news generation. Supervisor reconciliation could generate diverse yet coherent news angles.

### 7. PROPHET: An Inferable Future Forecasting Benchmark
- **Authors**: Multiple
- **Year**: 2025
- **arXiv**: 2504.01509
- **Key Contribution**: Introduces Causal Intervened Likelihood (CIL) to identify which prediction questions are actually answerable from available evidence. Filters questions into inferable (L1) vs. non-inferable (L2).
- **Methodology**: CIL measures causal support of news articles for prediction outcomes. Uses QwQ-32B for probability estimation. Evaluates naive vs. agentic RAG approaches.
- **Datasets**: 612 inferable + 43 non-inferable questions from Polymarket (Jan 2025). ~560 news articles per question from MediaCloud.
- **Results**: Agentic RAG outperforms naive RAG. GPT-4.1 achieves best Brier score (-3.20 improvement). Naive document concatenation is insufficient.
- **Code**: https://github.com/TZWwww/PROPHET
- **Relevance**: **High** — CIL provides principled method to validate whether generated future news is evidentially grounded. Essential for quality control.

### 8. KalshiBench: Evaluating Epistemic Calibration via Prediction Markets
- **Authors**: Lukas Nel (Lotus AI)
- **Year**: 2025
- **arXiv**: 2512.16030
- **Key Contribution**: Benchmark of 1,531 Kalshi prediction market questions for evaluating LLM calibration (not just accuracy). Temporally filtered to prevent knowledge contamination.
- **Datasets**: 300 evaluation questions across 13 categories from CFTC-regulated Kalshi exchange.
- **Results**: All frontier models are systematically overconfident. Best calibrated: Claude Opus 4.5 (ECE=0.120). Reasoning enhancements worsen calibration.
- **Relevance**: **Moderate-High** — highlights calibration challenges critical for credible future news. Dataset available on HuggingFace.

### 9. Fake Prediction Markets, Real Confidence Signals
- **Authors**: Todasco (SDSU)
- **Year**: 2025
- **arXiv**: 2512.05998
- **Key Contribution**: Tests whether framing LLM evaluation as a fictional prediction market (with LLMCoin currency) surfaces calibrated confidence signals. "Whale" bets (40K+ coins) correct ~99% of the time.
- **Results**: Betting mechanic creates legible confidence signal absent from binary outputs. Accuracy gains modest but stake size tracks confidence well.
- **Relevance**: **Moderate** — suggests financial framing can elicit better uncertainty quantification from LLMs, applicable to assigning confidence to generated news.

### 10. AI-Augmented Predictions: LLM Assistants Improve Human Forecasting Accuracy
- **Authors**: Schoenegger, Park, Karger, Trott, Tetlock
- **Year**: 2024
- **arXiv**: 2402.07862
- **Key Contribution**: Shows LLM assistants (even noisy ones) improve human forecasting by 24-28%. Superforecasting-prompted assistant improves accuracy by 41%.
- **Datasets**: N=991 participants, 6 forecasting questions.
- **Relevance**: **Moderate** — demonstrates human-LLM collaboration for forecasting, applicable to editorial workflows for future news.

### 11. Evaluating LLMs on Real-World Forecasting Against Expert Forecasters
- **Authors**: Janna Lu (GMU)
- **Year**: 2025
- **arXiv**: 2507.04562
- **Key Contribution**: Evaluates 12 frontier models on 464 Metaculus questions. Tests narrative prompting (fiction-style) vs. direct prompting.
- **Datasets**: 334 + 130 Metaculus questions, news from AskNews.
- **Results**: Frontier models surpass human crowd but still underperform expert forecasters. Narrative prompting decreases accuracy (important finding for news generation).
- **Relevance**: **Moderate-High** — narrative prompt finding is directly relevant: fiction framing may hurt forecast accuracy, suggesting separation of forecasting and narrative generation stages.

### 12. Prompt Engineering LLMs' Forecasting Capabilities
- **Authors**: Multiple
- **Year**: 2025
- **arXiv**: 2506.01578
- **Key Contribution**: Systematic comparison of prompt strategies for LLM forecasting including superforecaster persona and scratchpad prompting.
- **Relevance**: **Moderate** — provides prompt engineering best practices for the forecasting component.

### 13. From News to Forecast: Integrating Event Analysis in LLM-Based Time Series Forecasting
- **Authors**: Multiple (NeurIPS 2024)
- **Year**: 2024
- **arXiv**: 2409.17515
- **Key Contribution**: Uses LLMs and Generative Agents to integrate news events into time series forecasting with reflection mechanisms.
- **Relevance**: **Moderate** — demonstrates news-to-forecast pipeline, inverse of our forecast-to-news goal but methodologically informative.

---

## Common Methodologies

1. **RAG-based forecasting**: Retrieve news articles → feed to LLM with prediction question → generate probability (used in PROPHET, AIA Forecaster, ForecastBench submissions)
2. **Superforecaster persona prompting**: Instruct LLM to adopt Tetlock-style reasoning (used across most papers)
3. **Market-conditioned prompting**: Use prediction market prices as Bayesian priors for LLM updates (Mention Markets paper)
4. **Self-play + DPO fine-tuning**: Generate multiple reasoning traces, rank by outcome proximity, fine-tune (Outcome-Driven paper)
5. **Multi-agent ensembling**: Run multiple independent forecasting agents, reconcile with supervisor (AIA Forecaster)
6. **Post-hoc calibration**: Platt scaling / SVR to correct systematic biases like hedging toward 0.5 (AIA Forecaster, Log Probabilities paper)

## Standard Baselines

- **Random/Uninformed**: Brier score 0.25 (always predict 50%)
- **Human crowd**: Brier ~0.12-0.15
- **Superforecasters**: Brier ~0.08-0.10
- **Prediction market consensus**: Brier ~0.10-0.18 (varies by market liquidity)
- **Vanilla GPT-4o**: Brier ~0.19-0.24

## Evaluation Metrics

- **Brier Score**: Primary metric. BS = (1/N)Σ(p_i - o_i)². Lower is better.
- **Expected Calibration Error (ECE)**: Measures alignment between confidence and accuracy.
- **AvgMaxSim**: Semantic similarity between generated and real events (Time-R1).
- **Accuracy / F1**: Binary classification of event outcomes.

## Datasets in the Literature

| Dataset | Source | Size | Used In |
|---------|--------|------|---------|
| ForecastBench | Polymarket, Metaculus, Manifold + 5 others | 6,435 questions | ForecastBench, AIA Forecaster |
| Polymarket resolved questions | Polymarket | 12,100+ binary | Outcome-Driven FT, PROPHET |
| KalshiBench | Kalshi exchange | 1,531 questions | KalshiBench paper |
| Kalshi mention markets | Kalshi | 856 contracts | Mention Markets |
| Metaculus tournaments | Metaculus | 464+ questions | Lu 2025 |
| NYT articles + Time-Bench | New York Times | 200K+ articles | Time-R1 |
| MediaCloud news | MediaCloud | ~560 articles/question | PROPHET |

## Gaps and Opportunities

1. **No existing work directly generates full news articles conditioned on prediction market probabilities** — papers focus on probability estimation, not narrative generation
2. **Narrative prompting hurts forecast accuracy** (Lu 2025) — suggests forecasting and news writing should be separate pipeline stages
3. **LLMs are systematically overconfident** — calibration must be addressed before presenting probabilities in news
4. **Multi-event coherence is weak** — LLMs struggle with covariance reasoning (ForecastBench), critical for coherent news narratives
5. **Small models can match large ones** on temporal tasks (Time-R1 3B vs 671B) — enables cost-effective deployment

## Recommendations for Our Experiment

### Recommended Architecture
A **two-stage pipeline**:
1. **Forecasting stage**: Use prediction market data (Polymarket/Metaculus) as probability anchors. Apply RAG with recent news. Use superforecaster persona prompting. Apply post-hoc calibration (Platt scaling).
2. **News generation stage**: Condition on calibrated probabilities to generate plausible news articles. Use temporal grounding (Time-R1 approach). Evaluate with AvgMaxSim and human judgment.

### Recommended Datasets
1. **ForecastBench** — dynamic benchmark with diverse questions from multiple platforms
2. **KalshiBench** — 1,531 questions with ground truth for calibration evaluation
3. **Polymarket resolved markets** — large-scale binary outcomes for training/evaluation

### Recommended Baselines
1. Vanilla LLM generation without market conditioning (ablation)
2. Market-only baseline (report market consensus as "news")
3. RAG-only baseline (news retrieval without market signal)
4. Market-conditioned generation (MCP approach from Mention Markets)

### Recommended Metrics
1. **Brier Score** — for probability calibration of forecasts
2. **AvgMaxSim** — semantic similarity to real outcomes (Time-R1 style)
3. **Human evaluation** — plausibility, coherence, informativeness ratings
4. **ECE** — calibration quality of presented probabilities
