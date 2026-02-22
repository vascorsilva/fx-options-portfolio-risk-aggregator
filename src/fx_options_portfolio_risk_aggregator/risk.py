from __future__ import annotations

from datetime import date

from .models import Trade, TradeResults, PortfolioResults
from .pricing import delta_per_unit, price_per_unit, vega_per_unit
from .daycount import year_fraction, DayCount


def price_trade(trade: Trade, valuation_date: date, day_count: DayCount = DayCount.ACT_365) -> TradeResults:
    """
    Takes in Trade object, calculates PV, Delta, and Vega and returns TradeResults object.
    Assumes ACT/365 day counting convention by default.
    """

    if isinstance(trade.expiry, float):
        t = float(trade.expiry)
    
    else:
        if valuation_date is None:
            raise ValueError("valuation_date is required when Expiry is a date.")
        t = year_fraction(valuation_date, trade.expiry, day_count)
    

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


    vega_u = vega_per_unit(
        trade.spot,
        trade.strike,
        t,
        trade.rate_domestic,
        trade.rate_foreign,
        trade.vol,
    )


    return TradeResults(
        trade_id=trade.trade_id,
        underlying=trade.underlying,
        pv=pv_u * trade.notional,          # notional is foreign units so present value and greeks returned in domestic currency units.
        delta=delta_u * trade.notional,
        vega=vega_u * trade.notional,
        t=t
    )


def aggregate_portfolio(results: list[TradeResults]) -> PortfolioResults:
    return PortfolioResults(
        pv_total=sum(r.pv for r in results),
        delta_total=sum(r.delta for r in results),
        vega_total=sum(r.vega for r in results),
        n_trades=len(results)
    )