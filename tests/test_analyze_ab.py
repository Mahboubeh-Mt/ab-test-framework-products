import pandas as pd

from src.analyze_ab import analyze


def test_analyze_keys_and_types():
    df = pd.DataFrame(
        {
            "group": ["control"] * 500 + ["treatment"] * 500,
            "clicked": [0] * 450 + [1] * 50 + [0] * 430 + [1] * 70,  # 10% vs 14%
        }
    )
    stats = analyze(df)
    assert 0.09 < stats.control_ctr < 0.11
    assert 0.13 < stats.treatment_ctr < 0.15
    assert stats.abs_lift > 0
    assert 0 <= stats.p_value <= 1
