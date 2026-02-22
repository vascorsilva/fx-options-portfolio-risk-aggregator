from __future__ import annotations

from datetime import date
from enum import Enum


class DayCount(str, Enum):
    ACT_365 = "ACT/365"
    ACT_360 = "ACT/360"


def year_fraction(start: date, end: date, convention: DayCount) -> float:
    if end < start:
        raise ValueError("Expiry date before valuation date.")

    days = (end - start).days

    if convention == DayCount.ACT_365:
        return days / 365.0

    if convention == DayCount.ACT_360:
        return days / 360.0

    raise NotImplementedError(f"Convention '{convention}' not implemented")

