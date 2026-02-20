from __future__ import annotations

from datetime import date

from .daycount import years_in_fraction
from .models import Trade, TradeResults, PortfolioResults


def price_trade(trade: Trade, valuation_date: date) -> TradeResults():
    
    t = years_in_fraction(valuation_date, trade.expiry)
    

    pv_u = price_per_unit(
        trade.spot,
        trade.strike,
        t,
        trade.rate_domestic,
        trade.rate_foreign,
        trade.vol,
        trade.option_type.value
    )

    delta_u = delta_per_unit(
        trade.spot,
        trade.strike,
        t,
        trade.rate_domestic,
        trade.rate_foreign,
        trade.vol,
        trade.option_type.value
    )


    vega_u = delta_per_unit(
        trade.spot,
        trade.strike,
        t,
        trade.rate_domestic,
        trade.rate_foreign,
        trade.vol,
    )

    return TradeResult(
        trade_id=trade.trade_id,
        underlying=trade.underlying,
        pv=pv_u * trade.notional,          # notional is foreign units so present value and greeks returned in domestic currency units.
        delta=delta_u * trade.notional,
        vega=vega_u * trade.notional,
        t=t
    )



def aggregate_portfolio(results: List[TradeResults]) -> PortfolioResults:
    return PortfolioResult(
        pv_total=sum(r.pv for r in results),
        delta_total=sum(r.delta for r in results),
        vega_total=sum(r.vega for r in results),
        n_trades=len(results)
    )