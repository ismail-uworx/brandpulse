import pytest
from app.ingestion.cleaner import Cleaner
from app.ingestion.parser import Parser

def test_cleaner_strips_html_tags():
    raw_text = "<div>Hello <b>World</b></div>"
    assert Cleaner.clean(raw_text) == "Hello World"

def test_cleaner_unescapes_html_entities():
    raw_text = "Billing &amp; Payment Issues"
    assert Cleaner.clean(raw_text) == "Billing & Payment Issues"

def test_cleaner_collapses_whitespace():
    raw_text = "Too\n\tmany    spaces"
    assert Cleaner.clean(raw_text) == "Too many spaces"

def test_parser_normalizes_mock_data():
    raw_mock = {
        "author": "Ismail",
        "title": "Bug Report",
        "summary": "Details here",
        "timestamp": "2026-07-16"
    }
    parsed = Parser.parse_mock(raw_mock)
    assert parsed["author"] == "Ismail"
    assert parsed["text"] == "Bug Report Details here"
    assert parsed["source"] == "mock"