import pytest

from app.services.content_calendar_loader import CONTENT_CALENDAR_FILENAME
from app.services.knowledge_loader import CONTENT_CALENDAR_DIRNAME, KnowledgeLoadError, load_knowledge
from factories import build_sample_calendar


def test_load_knowledge_returns_expected_keys():
    kb = load_knowledge()

    assert "company_profile" in kb
    assert "brand_voice" in kb
    assert "hashtag_bank" in kb


def test_markdown_files_load_as_text():
    kb = load_knowledge()

    assert isinstance(kb["company_profile"], str)
    assert len(kb["company_profile"]) > 0


def test_yaml_files_load_as_parsed_data():
    kb = load_knowledge()

    assert isinstance(kb["hashtag_bank"], dict)


def test_missing_folder_raises_clear_error(tmp_path):
    missing_dir = tmp_path / "does_not_exist"

    with pytest.raises(KnowledgeLoadError, match="Knowledge folder not found"):
        load_knowledge(missing_dir)


def test_invalid_yaml_raises_clear_error(tmp_path):
    bad_file = tmp_path / "broken.yaml"
    bad_file.write_text("key: [unclosed", encoding="utf-8")

    with pytest.raises(KnowledgeLoadError, match="Invalid YAML"):
        load_knowledge(tmp_path)


def test_unsupported_file_types_are_ignored(tmp_path):
    (tmp_path / "notes.txt").write_text("ignored", encoding="utf-8")
    (tmp_path / "profile.md").write_text("# Hello", encoding="utf-8")

    kb = load_knowledge(tmp_path)

    assert "notes" not in kb
    assert kb["profile"] == "# Hello"


def test_content_calendar_key_is_empty_dict_when_no_calendar_file(tmp_path):
    kb = load_knowledge(tmp_path)

    assert kb[CONTENT_CALENDAR_DIRNAME] == {}


def test_content_calendar_loads_from_excel_file(tmp_path):
    calendar_dir = tmp_path / CONTENT_CALENDAR_DIRNAME
    calendar_dir.mkdir()
    build_sample_calendar(calendar_dir / CONTENT_CALENDAR_FILENAME)

    kb = load_knowledge(tmp_path)

    assert set(kb[CONTENT_CALENDAR_DIRNAME].keys()) == {"Week 1", "Week 2"}
    assert kb[CONTENT_CALENDAR_DIRNAME]["Week 1"]["Post 1"]["status"] == "Draft"


def test_content_calendar_load_failure_raises_knowledge_load_error(tmp_path):
    calendar_dir = tmp_path / CONTENT_CALENDAR_DIRNAME
    calendar_dir.mkdir()
    (calendar_dir / CONTENT_CALENDAR_FILENAME).write_text("not a real workbook", encoding="utf-8")

    with pytest.raises(KnowledgeLoadError, match="Invalid Excel file"):
        load_knowledge(tmp_path)


def test_real_knowledge_dir_content_calendar_is_a_dict():
    kb = load_knowledge()

    assert isinstance(kb[CONTENT_CALENDAR_DIRNAME], dict)
