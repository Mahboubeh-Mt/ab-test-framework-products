from __future__ import annotations

import argparse
import os

import pandas as pd

from .analyze_ab import analyze
from .generate_data import ABConfig, generate_synthetic_ab
from .visualize_results import plot_ctr_with_ci


def cmd_generate(args: argparse.Namespace) -> None:
    cfg = ABConfig(
        n=args.n,
        baseline=args.baseline,
        effect=args.effect,
        ratio=args.ratio,
        seed=args.seed,
    )
    df = generate_synthetic_ab(cfg)
    os.makedirs("data", exist_ok=True)
    out = "data/synthetic_ab.csv"
    df.to_csv(out, index=False)
    print(
        f"[OK] Wrote {out}  (rows={len(df)}, "
        f"baseline={args.baseline}, effect={args.effect})"
    )


def cmd_analyze(args: argparse.Namespace) -> None:
    df = pd.read_csv(args.path)
    stats = analyze(df)
    print("\n=== A/B Summary ===")
    print(f"Control CTR   : {stats.control_ctr*100:.2f}%")
    print(f"Treatment CTR : {stats.treatment_ctr*100:.2f}%")
    print(f"Abs Lift      : {stats.abs_lift*100:.2f} pp")
    print(f"Rel Lift      : {stats.rel_lift*100:.2f}x")
    print(f"p-value       : {stats.p_value:.4g}")
    print(
        "95% CI (pp)   : "
        f"[{stats.ci_low_pp*100:.2f}, {stats.ci_high_pp*100:.2f}]"
    )
    print("===================\n")


def cmd_plot(args: argparse.Namespace) -> None:
    df = pd.read_csv(args.path)
    out = plot_ctr_with_ci(df)
    print(f"[OK] Saved plot → {out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ab-test-framework-products",
        description="A/B testing toolkit",
    )
    sub = parser.add_subparsers(required=True)

    p_gen = sub.add_parser("generate", help="Create synthetic A/B dataset")
    p_gen.add_argument("--n", type=int, default=20000)
    p_gen.add_argument("--baseline", type=float, default=0.10)
    p_gen.add_argument("--effect", type=float, default=0.02)
    p_gen.add_argument("--ratio", type=float, default=0.5)
    p_gen.add_argument("--seed", type=int, default=7)
    p_gen.set_defaults(func=cmd_generate)

    p_an = sub.add_parser("analyze", help="Analyze A/B CSV (lift, p-value, CI)")
    p_an.add_argument("path", type=str)
    p_an.set_defaults(func=cmd_analyze)

    p_pl = sub.add_parser("plot", help="Plot CTRs with 95% CI")
    p_pl.add_argument("path", type=str)
    p_pl.set_defaults(func=cmd_plot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
