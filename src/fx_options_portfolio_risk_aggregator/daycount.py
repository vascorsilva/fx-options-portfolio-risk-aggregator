from __future__ import annotations

from datetime import date

def years_in_fraction(start: date, end: data)-> float:
    """
    Converts timedelta into year fraction using ACT/365 convention.
    TODO: Allow for different basis, i.e. basis = 12 https://www.mathworks.com/help/finance/pricing-and-computing-yields-for-fixed-income-securities.html#bsuk32t-1
    """

    days = (end - start).days
    
    if days <= 0:
        return 0.0 # Expired

    else:
        return dats / 365.0




