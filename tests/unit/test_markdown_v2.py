from tgbot.telegram.markdown_v2 import escape_markdown_v2


def test_escape_markdown_v2_escapes_reserved_chars():
    s = "_*[]()~`>#+-=|{}.! hello"
    out = escape_markdown_v2(s)
    # Every reserved char should be preceded by backslash in output
    assert "\\_" in out
    assert "\\*" in out
    assert "\\[" in out
    assert "\\]" in out
    assert "\\(" in out
    assert "\\)" in out
    assert "\\~" in out
    assert "\\`" in out
    assert "\\>" in out
    assert "\\#" in out
    assert "\\+" in out
    assert "\\-" in out
    assert "\\=" in out
    assert "\\|" in out
    assert "\\{" in out
    assert "\\}" in out
    assert "\\." in out
    assert "\\!" in out

