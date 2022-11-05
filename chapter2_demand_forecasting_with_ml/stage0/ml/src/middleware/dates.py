from datetime import date, timedelta
from typing import List


def dates_in_between_dates(
    date_from: date,
    date_to: date,
) -> List[date]:
    dates = []
    delta = date_to - date_from
    for i in range(delta.days + 1):
        d = date_from + timedelta(days=i)
        dates.append(d)
    return dates
