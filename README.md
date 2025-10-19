# ab-test-framework-products

**A clean, production-minded A/B testing framework** for product decisions.  
It simulates experiments, runs statistical analysis (two-proportion z-test + bootstrap CIs), and produces clear, decision-ready visuals.

[![CI](https://github.com/Mahboubeh-Mt/ab-test-framework-products/actions/workflows/ci.yml/badge.svg?branch=main&event=push&ts=3)](https://github.com/Mahboubeh-Mt/ab-test-framework-products/actions/workflows/ci.yml?query=branch%3Amain+event%3Apush)
[![codecov](https://codecov.io/gh/Mahboubeh-Mt/ab-test-framework-products/branch/main/graph/badge.svg)](https://codecov.io/gh/Mahboubeh-Mt/ab-test-framework-products)

## Why this project
- **Decisions, not just models:** hypothesis → analysis → recommendation  
- **Statistical rigor:** difference in proportions, p-values, 95% bootstrap CIs  
- **Engineering discipline:** clear structure, tests, linting, CI

## Quickstart
```bash
# 0) install
pip install -r requirements.txt

# 1) generate synthetic data (control vs. treatment)
python -m src.cli generate --n 20000 --baseline 0.10 --effect 0.025 --seed 7

# 2) analyze (lift, p-value, CIs)
python -m src.cli analyze data/synthetic_ab.csv

# 3) plot (saves to outputs/figures/)
python -m src.cli plot data/synthetic_ab.csv
```
### 👤 Author & Contact

**Mahboubeh Motaghi**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mahboubeh-motaghi-phd-58033759)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Profile-4285F4?logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=CkXNH2MAAAAJ&hl=en)
[![Email](https://img.shields.io/badge/Email-Contact-informational?logo=gmail&logoColor=white)](mailto:mahboubeh.motaghi@gmail.com)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)