from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest


@dataclass
class ABStats:
    control_ctr: float
    treatment_ctr: float
    abs_lift: float
    rel_lift: float
    p_value: float
    ci_low_pp: float
    ci_high_pp: float


def _bootstrap_diff_in_prop(
    df: pd.DataFrame,
    n_boot: int = 2000,
    seed: int | None = 7,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    ctrl = df[df["group"] == "control"]["clicked"].to_numpy()
    trt = df[df["group"] == "treatment"]["clicked"].to_numpy()

    diffs: list[float] = []
    n_ctrl, n_trt = len(ctrl), len(trt)
    for _ in range(n_boot):
        s_ctrl = rng.choice(ctrl, size=n_ctrl, replace=True)
        s_trt = rng.choice(trt, size=n_trt, replace=True)
        diffs.append(s_trt.mean() - s_ctrl.mean())
    low, high = np.percentile(diffs, [2.5, 97.5])
    return float(low), float(high)


def analyze(df: pd.DataFrame) -> ABStats:
    # aggregate
    summary = (
        df.groupby("group")["clicked"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "success"})
    )
    c_success = int(summary.loc["control", "success"])
    c_total = int(summary.loc["control", "count"])
    t_success = int(summary.loc["treatment", "success"])
    t_total = int(summary.loc["treatment", "count"])

    control_ctr = c_success / c_total
    treatment_ctr = t_success / t_total
    abs_lift = treatment_ctr - control_ctr
    rel_lift = abs_lift / control_ctr if control_ctr > 0 else np.nan

    # two-proportion z-test (H0: equal proportions)
    count = np.array([t_success, c_success])
    nobs = np.array([t_total, c_total])
    _, p_value = proportions_ztest(count, nobs, alternative="two-sided")

    # bootstrap CI (absolute percentage points)
    low, high = _bootstrap_diff_in_prop(df)
    return ABStats(
        control_ctr=control_ctr,
        treatment_ctr=treatment_ctr,
        abs_lift=abs_lift,
        rel_lift=rel_lift,
        p_value=float(p_value),
        ci_low_pp=low,
        ci_high_pp=high,
    )
