# Research Plan: News from the Future

## Motivation & Novelty Assessment

### Why This Research Matters
People constantly seek credible glimpses of future events—for investment decisions, policy planning, and general curiosity. Prediction markets aggregate crowd wisdom into probability estimates, but raw percentages lack narrative context. LLMs excel at generating coherent narratives but hallucinate freely when unconstrained. Combining both could produce *grounded* future news articles that are both informative and calibrated, filling a gap no existing system addresses.

### Gap in Existing Work
The literature review reveals extensive work on LLM forecasting (probability estimation) and prediction market analysis, but:
1. **No existing work generates full news articles conditioned on prediction market probabilities** (literature_review.md, Gap #1)
2. Narrative prompting actually *hurts* forecast accuracy (Lu 2025), suggesting forecasting and narrative generation must be separate pipeline stages
3. LLMs are systematically overconfident (KalshiBench), requiring calibration before embedding probabilities in news
4. Multi-event coherence is weak in current LLMs (ForecastBench)

### Our Novel Contribution
We build and evaluate an end-to-end system that:
1. Ingests prediction market data (questions, probabilities, context)
2. Generates plausible "news from the future" articles using LLMs
3. Tests whether market-conditioning improves article quality vs. unconditioned generation
4. Deploys as a functional web application

This is the **first systematic evaluation** of market-conditioned future news generation.

### Experiment Justification
- **Experiment 1 (Market conditioning ablation)**: Tests whether prediction market data improves generated article quality. Core hypothesis test.
- **Experiment 2 (Prompting strategies)**: Tests which prompting approach (direct, MCP-style, superforecaster persona) produces best articles. Identifies optimal pipeline configuration.
- **Experiment 3 (Calibration & plausibility on resolved markets)**: Uses resolved Polymarket events as ground truth to measure whether generated "future news" aligns with what actually happened. Validates the system end-to-end.

## Research Question
Can combining LLMs with prediction market data produce plausible, well-calibrated news articles about future events, and does market conditioning improve article quality over unconditioned generation?

## Background and Motivation
Prediction markets (Polymarket, Kalshi, Metaculus) provide calibrated probability estimates for future events. LLMs can generate fluent text. The hypothesis is that conditioning LLM generation on market probabilities produces more specific, grounded, and plausible future news than unconditioned generation.

## Hypothesis Decomposition
- **H1**: Market-conditioned articles are rated higher in plausibility than unconditioned articles
- **H2**: Market-conditioned articles are more specific and detailed than unconditioned articles
- **H3**: For resolved events, market-conditioned articles have higher semantic similarity to actual outcomes
- **H4**: Different prompting strategies (direct, MCP, persona) produce measurably different quality

## Proposed Methodology

### Approach
Two-stage pipeline inspired by the literature:
1. **Data stage**: Fetch prediction market questions with probabilities from Polymarket API
2. **Generation stage**: Generate future news articles using GPT-4.1 with different conditioning strategies
3. **Evaluation stage**: LLM-as-judge evaluation + semantic similarity for resolved events

### Experimental Steps
1. Load Polymarket resolved events (100 events with outcomes)
2. For each event, generate articles under 4 conditions:
   - **Baseline (No Market)**: Generate future news given only the topic/title
   - **Market-Conditioned (Direct)**: Include market probability directly in prompt
   - **Market-Conditioned (MCP)**: Use Market-Conditioned Prompting framework
   - **Superforecaster Persona**: Use superforecaster reasoning + market data
3. Evaluate all generated articles using:
   - LLM-as-judge (GPT-4.1) scoring on 5 dimensions: plausibility, specificity, coherence, informativeness, calibration
   - For resolved events: semantic similarity between generated article and actual outcome description
4. Statistical comparison across conditions

### Baselines
1. **No-Market Baseline**: LLM generates future news with topic only
2. **Market-Only Baseline**: Simply report the market probability as a one-liner
3. **Direct Conditioning**: Naive inclusion of market probability in prompt
4. **MCP (Market-Conditioned Prompting)**: Structured approach from Mention Markets paper

### Evaluation Metrics
- **Plausibility** (1-5): How believable is this as a real news article?
- **Specificity** (1-5): How detailed and specific are the claims?
- **Coherence** (1-5): Is the article internally consistent and well-structured?
- **Informativeness** (1-5): Does it provide useful information beyond the market question?
- **Calibration Quality** (1-5): Does the article appropriately convey uncertainty?
- **Semantic Similarity**: Cosine similarity between generated article and actual outcome (resolved events only)

### Statistical Analysis Plan
- Paired t-tests / Wilcoxon signed-rank for pairwise condition comparisons
- ANOVA / Kruskal-Wallis for overall condition differences
- Effect sizes (Cohen's d) for practical significance
- α = 0.05 with Bonferroni correction for multiple comparisons
- Bootstrap confidence intervals for mean scores

## Expected Outcomes
- Market-conditioned articles should score higher on plausibility and specificity
- MCP approach should outperform naive direct conditioning
- Superforecaster persona may improve calibration quality
- For resolved events, market-conditioned articles should have higher semantic similarity to actual outcomes

## Timeline and Milestones
1. Environment setup + data loading: 15 min
2. Pipeline implementation: 60 min
3. Run experiments (API calls): 30 min
4. Analysis and visualization: 30 min
5. Documentation: 20 min
6. Web app: 30 min

## Potential Challenges
- API rate limits → batch with delays, cache responses
- LLM-as-judge bias → use structured rubrics, multiple evaluation passes
- Resolved event descriptions may be sparse → supplement with web search context

## Success Criteria
1. Statistically significant improvement of market-conditioned over baseline (p < 0.05)
2. Generated articles are rated ≥3.5/5 on plausibility by LLM judge
3. Functional web application demonstrating the system
4. Clear documentation of methodology and results
