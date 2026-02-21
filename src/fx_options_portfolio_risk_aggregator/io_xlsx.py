from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .models import PortfolioResults, TradeResults


def read_excel_records(path: Path) -> list[dict[str, Any]]:
    df = pd.read_excel(path)
   
    return df.to_dict(orient="records")


def write_results(path: Path, trade_results: list[TradeResult], portfolio: PortfolioResult) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    trades_df = pd.DataFrame([r.model_dump() for r in trade_results])
    summary_df = pd.DataFrame(
        [
            {
                "pv_total": portfolio.pv_total,
                "delta_total": portfolio.delta_total,
                "vega_total": portfolio.vega_total,
                "n_trades": portfolio.n_trades,
            }
        ]
    )

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        trades_df.to_excel(writer, sheet_name="trade_results", index=False)
        summary_df.to_excel(writer, sheet_name="portfolio_summary", index=False)