from datetime import date
from pathlib import Path

from fx_options_portfolio_risk_aggregator.io_xlsx import read_excel_records
from fx_options_portfolio_risk_aggregator.models import Trade
from fx_options_portfolio_risk_aggregator.risk import aggregate_portfolio, price_trade


def test_end_to_end():
    repo_root = Path(__file__).resolve().parents[1]
    xlsx = repo_root / "data" / "fx_trades.xlsx"

    records = read_excel_records(xlsx)
    trades = [Trade.from_row(r) for r in records]

    results = [price_trade(t, date(2026, 2, 20)) for t in trades]
    portfolio = aggregate_portfolio(results)

    assert portfolio.n_trades == len(trades)
    assert portfolio.n_trades == 10
    assert portfolio.pv_total == portfolio.pv_total