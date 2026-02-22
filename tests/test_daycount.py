from datetime import date

from fx_options_portfolio_risk_aggregator.daycount import year_fraction, DayCount


def test_act_365():
    start = date(2026, 1, 1)
    end = date(2027, 1, 1)
    yf = year_fraction(start, end, DayCount.ACT_365)
    assert abs(yf - 1.0) < 1e-10


def test_act_360():
    start = date(2026, 1, 1)
    end = date(2027, 1, 1)
    yf = year_fraction(start, end, DayCount.ACT_360)
    assert abs(yf - 365/360) < 1e-10