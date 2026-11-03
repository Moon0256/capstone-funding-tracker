from datetime import date, timedelta

from app.dates import days_left


def test_deadline_far_in_the_future_has_days_left():
    deadline = date.today() + timedelta(days=100)
    assert days_left(deadline) > 0


def test_deadline_long_ago_has_passed():
    deadline = date.today() - timedelta(days=100)
    assert days_left(deadline) < 0


def test_deadline_today_has_zero_days_left():
    assert days_left(date.today()) == 0


def test_deadline_tomorrow_has_one_day_left():
    deadline = date.today() + timedelta(days=1)
    assert days_left(deadline) == 1


def test_deadline_yesterday_has_passed_by_one_day():
    deadline = date.today() - timedelta(days=1)
    assert days_left(deadline) == -1
