from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ABConfig:
    n: int = 20000
    baseline: float = 0.10  # control conversion prob
    effect: float = 0.02  # absolute lift for treatment (e.g., +2 pp)
    ratio: float = 0.5  # fraction in treatment
    seed: int | None = 42


def generate_synthetic_ab(cfg: ABConfig) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed)
    n_treat = int(cfg.n * cfg.ratio)
    n_ctrl = cfg.n - n_treat

    p_ctrl = cfg.baseline
    p_treat = max(min(cfg.baseline + cfg.effect, 1.0), 0.0)  # clamp [0,1]

    ctrl_clicked = rng.binomial(1, p_ctrl, size=n_ctrl)
    treat_clicked = rng.binomial(1, p_treat, size=n_treat)

    df = pd.DataFrame(
        {
            "group": (["control"] * n_ctrl) + (["treatment"] * n_treat),
            "clicked": np.concatenate([ctrl_clicked, treat_clicked]),
        }
    )
    return df
