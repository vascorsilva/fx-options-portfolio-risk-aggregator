from datetime import date

from pydantic import ValidationError

from fx_options_portfolio_risk_aggregator.models import Trade


def test_trade_parses_and_normalises_fileds():
    row = {
        "TradeID": "T1",
        "Underlying": "EUR/USD",
        "Notional": 1000000,
        "NotionalCurrency": "usd",
        "Spot": 1.10,
        "Strike": 1.12,
        "Vol": 0.10,
        "RateDomestic": 0.02,
        "RateForeign": 0.01,
        "Expiry": 0.5,
        "OptionType": "Call"
    }
    t = Trade.from_row(row)
    assert t.underlying == "EURUSD"
    assert t.notional_currency == "USD"
    assert t.option_type.value == "CALL"
    assert float(t.expiry) == 0.5


def test_trade_rejects_negative_notional():
    row = {
        "TradeID": "T1",
        "Underlying": "EUR/USD",
        "Notional": -1.0,
        "NotionalCurrency": "USD",
        "Spot": 1.10,
        "Strike": 1.12,
        "Vol": 0.10,
        "RateDomestic": 0.02,
        "RateForeign": 0.01,
        "Expiry": 0.5,
        "OptionType": "Put",
    }
    try:
        Trade.from_row(row)
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True

def test_trade_rejects_invalid_option_type():
    row = {
        "TradeID": "T1",
        "Underlying": "EUR/USD",
        "Notional": 1.0,
        "NotionalCurrency": "USD",
        "Spot": 1.10,
        "Strike": 1.12,
        "Vol": 0.10,
        "RateDomestic": 0.02,
        "RateForeign": 0.01,
        "Expiry": 0.5,
        "OptionType": "Binary",
    }
    try:
        Trade.from_row(row)
        assert False, "Expected a ValidationError"
    except ValidationError:
        assert True


def test_trade_with_date_expiry():
    row = {
        "TradeID": "T1",
        "Underlying": "EUR/USD",
        "Notional": 100000,
        "NotionalCurrency": "USD",
        "Spot": 1.10,
        "Strike": 1.12,
        "Vol": 0.10,
        "RateDomestic": 0.02,
        "RateForeign": 0.01,
        "Expiry": date(2027, 1, 1),
        "OptionType": "Call",
    }
    t = Trade.from_row(row)
    assert isinstance(t.expiry, date)