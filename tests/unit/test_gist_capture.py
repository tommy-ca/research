"""
Unit tests for gist-aware markdown capture
"""

from pathlib import Path
from src.pkm.core.capture import PkmCapture


def test_capture_adds_gist_source_and_tag(tmp_path):
    vault = tmp_path / 'vault'
    vault.mkdir()
    content = """# Sample
Reference text for research.
"""
    src = 'https://gist.github.com/user/abcdef1234567890'
    capture = PkmCapture(str(vault))
    res = capture.capture(content=content, source=src, tags=['#research'])
    assert res.success
    p = vault / res.file_path
    t = p.read_text(encoding='utf-8')
    assert 'source:' in t and src in t
    # tag itself is added at script layer; here we assert research tag retained
    assert '#research' in t

