import pytest
from freezegun import freeze_time

from main.main import give_dates_ago


@freeze_time("2023-08-15 12:00:00", tz_offset=0)
def test_give_dates_ago():
    assert give_dates_ago(day_ago=1) == ("2023-08-14 00:00:00", "2023-08-14 23:59:59")
    assert give_dates_ago(day_ago=2) == ("2023-08-13 00:00:00", "2023-08-13 23:59:59")


@freeze_time("2023-01-15 12:00:00", tz_offset=0)
def test_give_dates_months_ago_january():
    assert give_dates_ago(months_ago=1) == ("2022-12-01 00:00:00", "2022-12-31 23:59:59")


@freeze_time("2023-05-15 12:00:00", tz_offset=0)
def test_give_dates_months_ago():
    assert give_dates_ago(months_ago=1) == ("2023-04-01 00:00:00", "2023-04-30 23:59:59")


@freeze_time("2023-08-15 12:00:00", tz_offset=0)
def test_give_dates_ago_no_conditions():
    with pytest.raises(KeyError) as e:
        give_dates_ago()


if __name__ == '__main__':
    pytest.main()
