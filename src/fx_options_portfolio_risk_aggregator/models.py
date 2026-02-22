from __future__ import annotations

import numbers
from enum import Enum
from typing import Any, Mapping
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class OptionType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


def _normalise_option_type(value: Any) -> str:
    if value is None:
        raise ValueError("option_type required.")
    s = str(value).strip().upper()
    mapping = {
        "CALL": "CALL",
        "C": "CALL",
        "P": "PUT",
        "PUT": "PUT",
    }
    if s not in mapping:
        raise ValueError(f"invalid option_type: {value!r} (expected CALL/PUT)")
    return mapping[s]


class Trade(BaseModel):
    """
    TODO: Docstring
    """
    trade_id: str = Field(..., alias="TradeID", min_length=1)
    underlying: str = Field(..., alias="Underlying", min_length=6, max_length=7)
    notional: float = Field(..., alias="Notional", gt=0.0)
    notional_currency: str = Field(..., alias="NotionalCurrency", min_length=3, max_length=3)
    spot: float = Field(..., alias="Spot", gt=0.0)
    strike: float = Field(..., alias="Strike", gt=0.0)
    vol: float = Field(..., alias="Vol", ge=0.0)
    rate_domestic: float = Field(..., alias="RateDomestic")
    rate_foreign: float = Field(..., alias="RateForeign")
    expiry: float | date = Field(..., alias="Expiry")
    option_type: OptionType = Field(..., alias="OptionType")

    @field_validator("underlying")
    @classmethod
    def __normalise_underlying(cls, v: str) -> str:
        s = v.strip().upper().replace("/", "")
        if len(s) < 6:
            raise ValueError("Underlying must be fx currency pair notation e.g. EUR/USD or EURUSD")
        return s

    @field_validator("notional_currency")
    @classmethod
    def validate_ccy(cls, v: str)-> str:
        s = v.strip().upper()
        if len(s) != 3 or not s.isalpha():
            raise ValueError("NotionalCurrency must be a 3 letter currency code")
        return s

    @field_validator("vol")
    @classmethod
    def _check_vol(cls, v: float) -> float:
        if v > 5.0:
            raise ValueError("Vol seems too high. Expected something like 0.10 for 10% vol.")
        return v

    @field_validator("expiry", mode="before")
    @classmethod
    def _parse_expiry(cls, v: Any) -> float | date:
        if isinstance(v, numbers.Real) and not isinstance(v, bool):
            x = float(v)
            if x < 0.0:
                raise ValueError("Expiry must be >= 0.")
            return x

        if isinstance(v, datetime):
            return v.date()

        if isinstance(v, date):
            return v

        raise ValueError("Expiry must be float (TTM) or a date.")

    @field_validator("option_type", mode="before")
    @classmethod
    def _parse_option_type(cls, v: Any) -> OptionType:
        return OptionType(_normalise_option_type(v))

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Trade":
        return cls.model_validate(row)


class TradeResults(BaseModel):
    trade_id: str
    underlying: str
    pv: float
    delta: float
    vega: float
    t: float


class PortfolioResults(BaseModel):
    pv_total: float
    delta_total: float
    vega_total: float
    n_trades: int