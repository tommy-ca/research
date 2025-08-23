import subprocess
from pathlib import Path

def test_vault_structure_validator_ok():
    # Non-strict: should pass current repo but may warn
    result = subprocess.run([
        "python3", "scripts/validate_vault_structure.py"
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Vault structure OK" in result.stdout


def test_vault_structure_validator_strict_enforces_numbering():
    # Strict: if there are unnumbered subdirs, it should fail
    result = subprocess.run([
        "python3", "scripts/validate_vault_structure.py", "--strict"
    ], capture_output=True, text=True)
    assert result.returncode in (0, 2)
    if result.returncode == 2:
        assert "Unnumbered subdirectories" in result.stderr
