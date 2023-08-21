from datetime import timedelta, datetime, timezone

import pytest

from main.main import give_dates_ago


def test_give_dates_ago():
    date_format = "%Y-%m-%d"
    delta = timedelta(hours=3)
    time_now = (datetime.now(timezone.utc) + delta - timedelta(days=1)).strftime("%Y-%m-%d")

    assert give_dates_ago(day_ago=1) == (f"{time_now} 00:00:00", f"{time_now} 23:59:59")


if __name__ == '__main__':
    pytest.main()
