from src.generate_data import ABConfig, generate_synthetic_ab


def test_generate_shape_and_groups():
    df = generate_synthetic_ab(ABConfig(n=1000, baseline=0.1, effect=0.02, seed=1))
    assert len(df) == 1000
    assert set(df["group"].unique()) == {"control", "treatment"}
    assert set(df["clicked"].unique()).issubset({0, 1})
