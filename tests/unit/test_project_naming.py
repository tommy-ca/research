import os
import shutil
import subprocess
from pathlib import Path


def run_validator(projects_dir: Path) -> int:
    env = os.environ.copy()
    env["PROJECTS_DIR"] = str(projects_dir)
    result = subprocess.run([
        "bash", "scripts/validate_project_names.sh"
    ], env=env)
    return result.returncode


def test_validator_flags_non_compliant(tmp_path):
    # Arrange: create mixed project directories
    good = tmp_path / "01-good-project"
    good.mkdir(parents=True)
    legacy = tmp_path / "pkm-system"
    legacy.mkdir()
    bad = tmp_path / "research"
    bad.mkdir()

    # Act
    code = run_validator(tmp_path)

    # Assert: non-zero due to 'research'
    assert code != 0


def test_validator_passes_when_all_compliant(tmp_path):
    # Arrange: only compliant + allowed legacy
    (tmp_path / "01-core").mkdir()
    (tmp_path / "10-feature" ).mkdir()
    (tmp_path / "pkm-system").mkdir()  # allowed legacy stub

    # Act
    code = run_validator(tmp_path)

    # Assert
    assert code == 0

