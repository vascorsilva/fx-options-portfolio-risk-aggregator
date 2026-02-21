import math

from fx_options_portfolio_risk_aggregator.pricing import (
    price_per_unit,
    delta_per_unit,
    vega_per_unit
)


def test_put_call_parity():
    s = 1.10
    k = 1.12
    t = 0.5
    rd = 0.02
    rf = 0.01
    vol = 0.15

    c = price_per_unit(s, k, t, rd, rf, vol, "CALL")
    p = price_per_unit(s, k, t, rd, rf, vol, "PUT")

    rhs = s * math.exp(-rf * t) - k * math.exp(-rd * t)

    assert abs((c - p ) - rhs) < 1e-8


def test_delta_matches_finite_difference():
    s = 1.10
    k = 1.12
    t = 0.5
    rd = 0.02
    rf = 0.01
    vol = 0.15
    h = 1e-5

    price_plus_h = price_per_unit(s + h, k, t, rd, rf, vol, "CALL")
    price_minus_h = price_per_unit(s - h, k, t, rd, rf, vol, "CALL")
    
    fd = (price_plus_h - price_minus_h) / (2 * h)

    delta = delta_per_unit(s, k, t, rd, rf, vol, "CALL")

    assert abs(delta - fd) < 1e-6


def test_vega_matches_finite_difference():
    s = 1.10
    k = 1.12
    t = 0.5
    rd = 0.02
    rf = 0.01
    vol = 0.15
    h = 1e-5

    price_plus_h = price_per_unit(s, k, t, rd, rf, vol + h, "CALL")
    price_minus_h = price_per_unit(s, k, t, rd, rf, vol - h, "CALL")
    
    fd = (price_plus_h - price_minus_h) / (2 * h)

    vega = vega_per_unit(s, k, t, rd, rf, vol)

    assert abs(vega - fd) < 1e-6
