import pytest

from app.services.content_calendar_loader import (
    ContentCalendarLoadError,
    get_post,
    get_week,
    iter_posts,
    load_content_calendar,
)
from factories import build_sample_calendar


@pytest.fixture
def sample_calendar_path(tmp_path):
    return build_sample_calendar(tmp_path / "linkedin_content_calendar.xlsx")


def test_weeks_and_post_counts(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    assert set(calendar.keys()) == {"Week 1", "Week 2"}
    assert set(calendar["Week 1"].keys()) == {"Post 1", "Post 2", "Post 3"}
    assert set(calendar["Week 2"].keys()) == {"Post 1", "Post 2"}


def test_content_and_status_are_extracted(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    post = calendar["Week 1"]["Post 2"]
    assert post["content"] == "Caption for week 1 post 2"
    assert post["status"] == "Scheduled"


def test_image_is_extracted_for_post_with_image(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    image = calendar["Week 1"]["Post 1"]["image"]
    assert image is not None
    assert image["format"] == "png"
    assert isinstance(image["data"], bytes)
    assert len(image["data"]) > 0


def test_posts_without_images_have_none(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    assert calendar["Week 1"]["Post 2"]["image"] is None
    assert calendar["Week 2"]["Post 1"]["image"] is None


def test_get_week_and_get_post_accept_int_or_string(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    assert get_week(calendar, 1) == calendar["Week 1"]
    assert get_week(calendar, "Week 2") == calendar["Week 2"]

    assert get_post(calendar, 1, 2)["status"] == "Scheduled"
    assert get_post(calendar, "Week 2", "Post 1")["content"] == "Caption for week 2 post 1"


def test_get_post_returns_none_for_missing_slot(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    assert get_post(calendar, 1, 4) is None
    assert get_post(calendar, 99, 1) is None


def test_iter_posts_covers_every_planned_post(sample_calendar_path):
    calendar = load_content_calendar(sample_calendar_path)

    posts = list(iter_posts(calendar))

    assert len(posts) == 5
    assert ("Week 1", "Post 1", calendar["Week 1"]["Post 1"]) in posts
    assert ("Week 2", "Post 2", calendar["Week 2"]["Post 2"]) in posts


def test_missing_file_returns_empty_calendar(tmp_path):
    calendar = load_content_calendar(tmp_path / "does_not_exist.xlsx")

    assert calendar == {}


def test_corrupt_file_raises_clear_error(tmp_path):
    bad_file = tmp_path / "broken.xlsx"
    bad_file.write_text("this is not a real xlsx file", encoding="utf-8")

    with pytest.raises(ContentCalendarLoadError, match="Invalid Excel file"):
        load_content_calendar(bad_file)
