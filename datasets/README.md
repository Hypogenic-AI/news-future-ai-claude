# Downloaded Datasets

This directory contains datasets for the research project. Large data files are NOT
committed to git due to size. Follow the download instructions below.

## Dataset 1: KalshiBench

### Overview
- **Source**: HuggingFace (`2084Collective/kalshibench-v2`)
- **Size**: 1,531 prediction market questions
- **Format**: HuggingFace Dataset (Arrow)
- **Task**: Binary forecasting / calibration evaluation
- **Categories**: Sports, Politics, Entertainment, Companies, Elections, Mentions, Crypto, Climate/Weather, Financials, World, Economics, Social
- **License**: See HuggingFace page

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("2084Collective/kalshibench-v2")
dataset.save_to_disk("datasets/kalshibench/data")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/kalshibench/data")
print(dataset['train'][0])
```

### Sample Data
Each record contains: `id`, `question`, `description`, `category`, `close_time`, `ground_truth` (yes/no), `market_probability`, `series_ticker`, `source`.

See `datasets/kalshibench/samples.json` for examples.

---

## Dataset 2: ForecastBench Questions

### Overview
- **Source**: GitHub (`forecastingresearch/forecastbench-datasets`)
- **Size**: ~500 questions per biweekly set, continuously updated
- **Format**: JSON
- **Task**: Binary forecasting
- **Sources**: Manifold Markets, Polymarket, Metaculus, RFI, ACLED, DBnomics, FRED, Wikipedia, Yahoo Finance
- **License**: CC BY-SA 4.0

### Download Instructions

```bash
git clone https://github.com/forecastingresearch/forecastbench-datasets.git
```

### Loading the Dataset

```python
import json
with open("code/forecastbench-datasets/datasets/question_sets/2026-03-01-llm.json") as f:
    data = json.load(f)
questions = data["questions"]
print(f"Number of questions: {len(questions)}")
```

### Notes
- Questions are updated nightly
- Includes resolution sets for scoring
- Human forecast sets available for comparison
- Local copy in `datasets/forecastbench/sample_questions.json`

---

## Dataset 3: Polymarket Resolved Events

### Overview
- **Source**: Polymarket Gamma API
- **Size**: 100 top resolved events (expandable via API)
- **Format**: JSON
- **Task**: Binary outcome prediction
- **License**: Public API data

### Download Instructions

```python
import requests, json
url = "https://gamma-api.polymarket.com/events?closed=true&limit=100&order=volume&ascending=false"
r = requests.get(url)
data = r.json()
with open("datasets/polymarket/top_resolved_events.json", "w") as f:
    json.dump(data, f, indent=2)
```

For larger datasets, see:
- **Kaggle**: `ismetsemedov/polymarket-prediction-markets`
- **GitHub**: `Jon-Becker/prediction-market-analysis` (largest public Polymarket + Kalshi dataset)
- **API**: `predictiondata.dev` (commercial, 10B+ tick-level updates)

### Notes
- Polymarket API provides real-time and historical data
- For the outcome-driven fine-tuning approach (paper 2502.05253), 12,100 binary questions were collected
- Volume data helps identify high-quality, liquid markets

---

## Dataset 4: Metaculus Questions (via ForecastBench)

### Overview
- **Source**: Metaculus API (requires authentication) / ForecastBench
- **Size**: 464+ questions in Lu (2025) dataset, thousands more available
- **Format**: JSON via API
- **Task**: Binary and continuous forecasting

### Download Instructions

Metaculus API requires authentication:
```python
import requests
headers = {"Authorization": "Token YOUR_TOKEN_HERE"}
url = "https://www.metaculus.com/api/questions/?status=resolved&type=binary&limit=100"
r = requests.get(url, headers=headers)
```

Alternatively, use ForecastBench which aggregates Metaculus questions without authentication.

### Notes
- Free account registration at metaculus.com
- API documentation at metaculus.com/api/
- ForecastBench already includes Metaculus questions in its question sets
