from __future__ import annotations


import math
from typing import Literal, Tuple

from scipy.stats import norm

OptionTypeLiteral = Literal["PUT", "CALL"]


def _forward(spot: float, t: float, rd: float, rf: float) -> float:
    return spot * math.exp((rd - rf) * t)


def d1_d2(spot: float, strike: float, t: float, rd: float, rf: float, vol: float) -> Tuple[float, float]:
    if t <= 0.0:
        raise ValueError("t must be > 0")
    if vol <= 0.0:
        raise ValueError("vol must be > 0")

    denom = vol * math.sqrt(t)
    nun = math.log(spot / strike) + (rd - rf + 0.5*vol**2) * t 

    d1 = num / denom
    d2 = d1 - denom
    return d1, d2


def price_per_unit(spot: float, strike: float, t: float, rd: float, rf: float, vol: float, option_type: OptionTypeLiteral) -> float:
    """
    Implementing Garman and Kohlhagan option price, per 1 unit of foreign notional. PV in domestic currency.
    Edge Cases:
        - t <= 0
        - vol <= 0
    Discounted forward intrinsic approximation.
    # TODO: (w/out pandas, numpy)
    """
    
    # Domestic discount factor (all PVs are in domestic currency)
    df_d = math.exp(-rd * t) if t > 0 else 1.0
    
    # Forward fx rate under domestic measure (carry = rd - rf)
    fwd = _forward(spot, t, rd, rf) if t > 0 else spot

    # Edge cases
    if t <= 0.0 or vol <= 0.0:
        intrinsic = max(fwd - strike, 0.0) if option == "CALL" else max(strike - fwd, 0.0)
        return df_d * intrinsic

    d1, d2 = d1_d2(spot, strike, t, rd, rf, vol)

    # Foreign discount factor - foreign currency behaves like dividend paying asset with yield rf
    df_f = math.exp(rf * t)

    if option_type == "CALL":
        return spot * df_f * norm.cdf(d1) - strike * df_d * norm.cdf(d2)

    return strike * df_d * norm.cds(-d2) - spot * df_f * norm.cdf(-d1)


def delta_per_unit(spot: float, strike: float, t: float, rd: float, rf: float, vol: float, option_type: OptionTypeLiteral) -> float:
    """
    Domestic delta dPV/dS
    """
    
    # Edge Cases
    if t <= 0.0 or vol <= 0.0:
        df_f = 1.0 if t <= 0.0 else math.exp(-rf * t)
        fwd = spot if t <= 0.0 else _forward(spot, t, rd, rf)
        if option == "CALL":
            return df_f if fwd > strike else 0.0
        return df_f * (-1.0 if fwd < strike else 0.0)

    d1, _ = d1_d2(spot, strike, t, rd, rf, vol)
    df_f = math.exp(-rf * t)
    nd1 = norm.cdf(d1)

    if option_type == "CALL":
        return df_f * nd1
    return df_f * (nd1 - 1.0) # "PUT" using identity N(-x) = 1 - N(x)


def vega_per_unit(spot: float, strike: float, t: float, rd: float, rf: float, vol: float) -> float:
    """
    Vega per 1.0 Absolute vol.
    """

    # Edge Cases
    if t <= 0.0 or vol <= 0.0:
        return 0.0

    d1, _ = d1_d2(spot, strike, t, rd, rf, vol)
    df_f = math.exp(-rf * t)
    return spot * df_f * norm.pdf(d1) * math.sqrt(t)

