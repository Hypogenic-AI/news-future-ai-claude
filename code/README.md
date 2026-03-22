# Cloned Repositories

## Repo 1: ForecastBench
- **URL**: https://github.com/forecastingresearch/forecastbench
- **Purpose**: Dynamic forecasting benchmark for LLMs. Reference implementation for question generation, submission, and scoring.
- **Location**: code/forecastbench/
- **Key files**: Submission scripts, question generation pipeline, scoring functions
- **Notes**: ICLR 2025 paper. Standard benchmark for evaluating LLM forecasting accuracy.

## Repo 2: ForecastBench Datasets
- **URL**: https://github.com/forecastingresearch/forecastbench-datasets
- **Purpose**: Nightly-updated question sets, resolution sets, and human/LLM forecast datasets.
- **Location**: code/forecastbench-datasets/
- **Key files**: `datasets/question_sets/*.json`, `datasets/resolution_sets/*.json`, `datasets/forecast_sets/`
- **Notes**: CC BY-SA 4.0 license. Contains human (superforecaster + public) forecasts for comparison.

## Repo 3: Polymarket Agents
- **URL**: https://github.com/Polymarket/agents
- **Purpose**: Official developer framework for building AI agents that trade on Polymarket prediction markets.
- **Location**: code/polymarket-agents/
- **Key files**: Agent architecture, Polymarket API connectors, ChromaDB for news vectorization, Gamma API client.
- **Notes**: MIT license. Provides infrastructure for retrieving market data, news articles, querying LLMs, and executing trades.

## Repo 4: Time-R1
- **URL**: https://github.com/ulab-uiuc/Time-R1
- **Purpose**: Temporal reasoning model that generates future news headlines. Progressive RL training with GRPO.
- **Location**: code/time-r1/
- **Key files**: Training scripts, reward functions, Time-Bench dataset, evaluation code.
- **Notes**: 3B model matching 671B on temporal tasks. HuggingFace models available. Directly applicable to future news generation.

## Repo 5: PROPHET Benchmark
- **URL**: https://github.com/TZWwww/PROPHET
- **Purpose**: Future forecasting benchmark with Causal Intervened Likelihood (CIL) for evidence quality validation.
- **Location**: code/prophet/
- **Key files**: CIL computation, RAG evaluation pipeline, Polymarket question dataset.
- **Notes**: 612 inferable questions from Polymarket with ~560 news articles each.

## Repo 6: Metaculus Forecasting Tools
- **URL**: https://github.com/Metaculus/forecasting-tools
- **Purpose**: Framework for building AI forecasting bots for Metaculus. API wrapper and tools.
- **Location**: code/metaculus-forecasting-tools/
- **Key files**: API client, question retrieval, forecast submission, Streamlit interface.
- **Notes**: Official Metaculus repository. Useful for accessing questions and submitting forecasts.

## Repo 7: Prediction Market Analysis
- **URL**: https://github.com/Jon-Becker/prediction-market-analysis
- **Purpose**: Largest publicly available dataset of Polymarket and Kalshi market and trade data.
- **Location**: code/prediction-market-analysis/
- **Key files**: Data collection scripts, analysis tools. Full data available as data.tar.zst from Cloudflare R2.
- **Notes**: Comprehensive data framework covering both major US prediction market platforms.
