# FX Options Portfolio Risk Aggregator

Prod-oriented Python risk engine to:
- load an FX options portfolio from Excel
- validate inputs (Pydantic)
- compute PV, Delta and Vega (Garman–Kohlhagen)
- export trade-level results and portfolio aggregates

## Quickstart
```bash
python3 -m venv .venv-fxopra
source .venv-fxopra/bin/activate
pip install -r requirements.txt
pytest


