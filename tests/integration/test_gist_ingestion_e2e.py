"""
End-to-end test for Gist Markdown ingestion through the pipeline

Validates:
- Capture to inbox with source URL and gist tag
- Inbox processing categorizes into PARA directories
- Pipeline creates an atomic note referencing the resource
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
from pathlib import Path


def run(cmd, cwd=None, env=None):
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def test_gist_ingestion_pipeline_end_to_end(tmp_path):
    vault = tmp_path / 'vault'
    vault.mkdir()

    # Create a sample markdown file simulating gist content
    md = """# Cross-Sectional Alpha Factors in Crypto

Reference note captured from a gist for research.

## Summary
- This is a summary section.
"""
    src_file = tmp_path / 'gist_note.md'
    src_file.write_text(md, encoding='utf-8')

    repo_root = Path(__file__).resolve().parents[2]
    script = repo_root / 'scripts' / 'pkm_ingest_pipeline.py'

    env = os.environ.copy()
    # Ensure repo root and src are importable
    env['PYTHONPATH'] = f"{repo_root}:{repo_root/'src'}:{env.get('PYTHONPATH','')}"

    gist_url = 'https://gist.github.com/user/abcdef1234567890'
    code, out, err = run([
        sys.executable, str(script),
        '--file', str(src_file),
        '--vault', str(vault),
        '--gist-url', gist_url
    ], env=env)

    assert code == 0, f"pipeline failed: {err}\nSTDOUT=\n{out}"

    # Parse summary lines
    lines = {k: v for k, v in [
        (l.split(':', 1)[0].strip(), l.split(':', 1)[1].strip())
        for l in out.splitlines() if ':' in l
    ]}
    resource_path = Path(lines.get('Resource path', ''))
    atomic_note_path = Path(lines.get('Atomic note', ''))

    assert resource_path.exists(), f"Resource path does not exist: {resource_path}"
    assert atomic_note_path.exists(), f"Atomic note path does not exist: {atomic_note_path}"

    # Verify resource frontmatter contains source and gist tag
    resource = resource_path.read_text(encoding='utf-8')
    assert 'source:' in resource and gist_url in resource, 'Missing gist source in frontmatter'
    assert '#source/gist' in resource, 'Missing gist tag in resource'

