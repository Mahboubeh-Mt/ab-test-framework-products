from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd

from .analyze_ab import analyze

def plot_ctr_with_ci(df: pd.DataFrame, out_path: str = "outputs/figures/ab_ctr.png") -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    stats = analyze(df)
    groups = ["Control", "Treatment"]
    ctrs = [stats.control_ctr, stats.treatment_ctr]

    # Simple bar chart (percent)
    plt.figure(figsize=(6, 4))
    plt.bar(groups, [c * 100 for c in ctrs])
    plt.ylabel("Conversion Rate (%)")
    plt.title("A/B Test – Conversion Rates")

    # Subtitle-style annotation
    subtitle = (
        f"Lift: {stats.abs_lift * 100:.2f} pp "
        f"(p={stats.p_value:.3g}; 95% CI: {stats.ci_low_pp * 100:.2f}–{stats.ci_high_pp * 100:.2f} pp)"
    )
    plt.suptitle(subtitle, y=0.97, fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return out_path
