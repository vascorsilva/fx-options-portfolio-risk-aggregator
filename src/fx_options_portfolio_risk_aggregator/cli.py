from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from pydantic import ValidationError

from .io_xlsx import read_excel_records, write_results
from .models import Trade
from .risk import aggregate_portfolio, price_trade
from .daycount import DayCount


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FX Options Portfolio Risk Aggregator (GK model)")
    parser.add_argument("--input", required=True, type=Path, help="Input Excel path")
    parser.add_argument("--output", required=True, type=Path, help="Output Excel path")
    parser.add_argument("--valuation-date", type=_parse_date, default=None, help="YYYY-MM-DD (Required if Expiry is a date)")
    parser.add_argument("--day-count", type=str, default="ACT/365", help="Day count convention (ACT/365, ACT/360)")
    parser.add_argument("--skip-invalid", action="store_true", help="Skip invalid rows instead of failing")

    args = parser.parse_args(argv)

    records = read_excel_records(args.input)

    day_count = DayCount(args.day_count)

    trades: list[Trade] = []
    errors: list[str] = []

    for i, row in enumerate(records, start=1):
        try:
            trades.append(Trade.from_row(row))
        except ValidationError as e:
            msg = f"Row {i}: {e.errors()}"
            errors.append(msg)
            if not args.skip_invalid:
                raise

    results = [price_trade(t, args.valuation_date, day_count) for t in trades]
    portfolio = aggregate_portfolio(results)
    write_results(args.output, results, portfolio)

    if errors:
        print(f"Skipped {len(errors)} invalid rows.")
    print(f"Priced {len(results)} trades. Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
