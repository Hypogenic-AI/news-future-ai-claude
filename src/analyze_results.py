"""Analyze experiment results with statistical tests and generate visualizations."""

import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

WORKSPACE = Path("/workspaces/news-future-ai-claude")
RESULTS_DIR = WORKSPACE / "results"
PLOTS_DIR = RESULTS_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)


def load_results():
    """Load experiment results into a DataFrame."""
    path = RESULTS_DIR / "experiment_results.json"
    with open(path) as f:
        data = json.load(f)
    return pd.DataFrame(data)


def descriptive_stats(df):
    """Compute descriptive statistics per condition."""
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy", "semantic_similarity"]
    conditions = ["no_market", "direct_market", "mcp", "superforecaster"]

    stats_data = []
    for cond in conditions:
        subset = df[df["condition"] == cond]
        for metric in metrics:
            vals = subset[metric].values
            stats_data.append({
                "condition": cond,
                "metric": metric,
                "mean": np.mean(vals),
                "std": np.std(vals),
                "median": np.median(vals),
                "min": np.min(vals),
                "max": np.max(vals),
                "n": len(vals),
            })
    return pd.DataFrame(stats_data)


def run_statistical_tests(df):
    """Run pairwise comparisons between conditions."""
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy", "semantic_similarity"]
    baseline = "no_market"
    treatment_conditions = ["direct_market", "mcp", "superforecaster"]

    test_results = []
    for metric in metrics:
        baseline_vals = df[df["condition"] == baseline][metric].values

        # Kruskal-Wallis across all conditions
        groups = [df[df["condition"] == c][metric].values for c in df["condition"].unique()]
        kw_stat, kw_p = stats.kruskal(*groups)

        for treat in treatment_conditions:
            treat_vals = df[df["condition"] == treat][metric].values

            # Wilcoxon signed-rank test (paired, non-parametric)
            try:
                w_stat, w_p = stats.wilcoxon(treat_vals, baseline_vals)
            except ValueError:
                w_stat, w_p = 0, 1.0

            # Effect size (Cohen's d)
            pooled_std = np.sqrt((np.std(baseline_vals)**2 + np.std(treat_vals)**2) / 2)
            cohens_d = (np.mean(treat_vals) - np.mean(baseline_vals)) / pooled_std if pooled_std > 0 else 0

            test_results.append({
                "metric": metric,
                "comparison": f"{treat} vs {baseline}",
                "baseline_mean": np.mean(baseline_vals),
                "treatment_mean": np.mean(treat_vals),
                "diff": np.mean(treat_vals) - np.mean(baseline_vals),
                "cohens_d": cohens_d,
                "wilcoxon_stat": w_stat,
                "wilcoxon_p": w_p,
                "kruskal_wallis_p": kw_p,
                "significant_005": w_p < 0.05,
                "significant_bonferroni": w_p < 0.05 / (len(metrics) * len(treatment_conditions)),
            })

    return pd.DataFrame(test_results)


def plot_condition_comparison(df):
    """Create bar chart comparing conditions across metrics."""
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy"]
    conditions = ["no_market", "direct_market", "mcp", "superforecaster"]
    labels = {"no_market": "No Market", "direct_market": "Direct", "mcp": "MCP", "superforecaster": "Superforecaster"}

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(metrics))
    width = 0.2

    for i, cond in enumerate(conditions):
        subset = df[df["condition"] == cond]
        means = [subset[m].mean() for m in metrics]
        stds = [subset[m].std() for m in metrics]
        ax.bar(x + i * width, means, width, yerr=stds, label=labels[cond],
               capsize=3, alpha=0.85)

    ax.set_ylabel("Score (1-5)")
    ax.set_title("Article Quality by Condition and Metric")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels([m.capitalize() for m in metrics])
    ax.legend()
    ax.set_ylim(0, 5.5)
    ax.axhline(y=3, color='gray', linestyle='--', alpha=0.5, label='Neutral')
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "condition_comparison.png", dpi=150)
    plt.close()
    print(f"  Saved condition_comparison.png")


def plot_semantic_similarity(df):
    """Plot semantic similarity by condition."""
    conditions = ["no_market", "direct_market", "mcp", "superforecaster"]
    labels = {"no_market": "No Market", "direct_market": "Direct", "mcp": "MCP", "superforecaster": "Superforecaster"}

    fig, ax = plt.subplots(figsize=(8, 5))
    data = [df[df["condition"] == c]["semantic_similarity"].values for c in conditions]

    bp = ax.boxplot(data, labels=[labels[c] for c in conditions], patch_artist=True)
    colors = sns.color_palette("muted", len(conditions))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    ax.set_ylabel("Semantic Similarity (0-1)")
    ax.set_title("Semantic Similarity to Actual Outcome by Condition")
    ax.set_ylim(0, 1.1)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "semantic_similarity.png", dpi=150)
    plt.close()
    print(f"  Saved semantic_similarity.png")


def plot_radar_chart(df):
    """Create radar chart of average scores per condition."""
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy"]
    conditions = ["no_market", "direct_market", "mcp", "superforecaster"]
    labels = {"no_market": "No Market", "direct_market": "Direct", "mcp": "MCP", "superforecaster": "Superforecaster"}

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    colors = sns.color_palette("muted", len(conditions))
    for i, cond in enumerate(conditions):
        subset = df[df["condition"] == cond]
        values = [subset[m].mean() for m in metrics]
        values += values[:1]
        ax.fill(angles, values, alpha=0.15, color=colors[i])
        ax.plot(angles, values, 'o-', label=labels[cond], color=colors[i], linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([m.capitalize() for m in metrics])
    ax.set_ylim(0, 5)
    ax.set_title("Quality Profile by Condition", pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "radar_chart.png", dpi=150)
    plt.close()
    print(f"  Saved radar_chart.png")


def plot_heatmap(df):
    """Create heatmap of mean scores."""
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy", "semantic_similarity"]
    conditions = ["no_market", "direct_market", "mcp", "superforecaster"]
    labels = {"no_market": "No Market", "direct_market": "Direct", "mcp": "MCP", "superforecaster": "Superforecaster"}

    matrix = np.zeros((len(conditions), len(metrics)))
    for i, cond in enumerate(conditions):
        subset = df[df["condition"] == cond]
        for j, metric in enumerate(metrics):
            matrix[i, j] = subset[metric].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    im = sns.heatmap(
        matrix, annot=True, fmt=".2f", cmap="YlOrRd",
        xticklabels=[m.capitalize().replace("_", " ") for m in metrics],
        yticklabels=[labels[c] for c in conditions],
        ax=ax, vmin=0, vmax=5,
    )
    ax.set_title("Mean Scores Heatmap")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "heatmap.png", dpi=150)
    plt.close()
    print(f"  Saved heatmap.png")


def plot_composite_score(df):
    """Plot composite score (mean of all 5 quality dimensions) by condition."""
    metrics = ["plausibility", "specificity", "coherence", "informativeness", "accuracy"]
    df_copy = df.copy()
    df_copy["composite"] = df_copy[metrics].mean(axis=1)

    conditions = ["no_market", "direct_market", "mcp", "superforecaster"]
    labels = {"no_market": "No Market", "direct_market": "Direct", "mcp": "MCP", "superforecaster": "Superforecaster"}

    fig, ax = plt.subplots(figsize=(8, 5))
    data = [df_copy[df_copy["condition"] == c]["composite"].values for c in conditions]

    bp = ax.boxplot(data, labels=[labels[c] for c in conditions], patch_artist=True)
    colors = sns.color_palette("muted", len(conditions))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    # Add means
    means = [np.mean(d) for d in data]
    ax.scatter(range(1, len(conditions)+1), means, color='red', zorder=5, s=60, marker='D', label='Mean')

    ax.set_ylabel("Composite Quality Score (1-5)")
    ax.set_title("Overall Article Quality by Condition")
    ax.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "composite_score.png", dpi=150)
    plt.close()
    print(f"  Saved composite_score.png")


def run_analysis():
    """Run full analysis pipeline."""
    print("Loading results...")
    df = load_results()
    print(f"  {len(df)} evaluations loaded")

    print("\nDescriptive statistics:")
    stats_df = descriptive_stats(df)
    print(stats_df.to_string(index=False))

    print("\nStatistical tests:")
    tests_df = run_statistical_tests(df)
    print(tests_df[["metric", "comparison", "diff", "cohens_d", "wilcoxon_p", "significant_005"]].to_string(index=False))

    print("\nGenerating visualizations...")
    plot_condition_comparison(df)
    plot_semantic_similarity(df)
    plot_radar_chart(df)
    plot_heatmap(df)
    plot_composite_score(df)

    # Save analysis results
    stats_df.to_csv(RESULTS_DIR / "descriptive_stats.csv", index=False)
    tests_df.to_csv(RESULTS_DIR / "statistical_tests.csv", index=False)
    print(f"\nAnalysis saved to {RESULTS_DIR}/")

    return df, stats_df, tests_df


if __name__ == "__main__":
    df, stats_df, tests_df = run_analysis()
