import json
import subprocess
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.unit
def test_settings_registers_compound_agent_and_hooks():
    settings_path = ROOT / ".claude" / "settings.json"
    data = json.loads(settings_path.read_text())

    # Agent registration
    agents = data.get("agents", {})
    assert "compound" in agents, "compound agent missing in settings"
    assert agents["compound"]["enabled"] is True
    assert isinstance(agents["compound"].get("tools", []), list)
    assert "Read" in agents["compound"]["tools"], "compound tools should include Read"

    # Hooks include CE prompts
    hooks = data.get("hooks", {}).get("UserPromptSubmit", [])
    assert hooks, "UserPromptSubmit hooks missing"
    prompts = hooks[0]["matcher"]["prompts"]
    for p in ["/ce-plan", "/ce-exec", "/ce-review", "/ce-pr"]:
        assert p in prompts, f"{p} missing from hooks prompts"


def _load_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text()
    assert text.startswith("---\n"), f"{md_path} missing YAML frontmatter"
    _, fm, _ = text.split("---\n", 2)
    return yaml.safe_load(fm)


@pytest.mark.unit
def test_ce_commands_have_valid_frontmatter_and_size():
    commands_dir = ROOT / ".claude" / "commands"
    allowed_agents = {"research", "synthesis", "compound"}

    for name in ["ce-plan.md", "ce-exec.md", "ce-review.md", "ce-pr.md"]:
        p = commands_dir / name
        assert p.exists(), f"missing command file: {name}"
        # Size constraint (SPEC: <= 50 lines)
        lines = p.read_text().strip().splitlines()
        assert len(lines) <= 50, f"{name} exceeds 50 line limit"

        fm = _load_frontmatter(p)
        assert fm.get("name"), f"{name} missing name"
        pattern = fm.get("pattern", "")
        assert pattern.startswith("/"), f"{name} pattern must start with /"
        assert fm.get("agent") in allowed_agents, f"{name} has invalid agent"


@pytest.mark.integration
def test_router_routes_ce_commands_to_compound(tmp_path):
    router = ROOT / ".claude" / "hooks" / "router.sh"
    cmd = f"bash {router} '/ce-plan ship feature'"
    out = subprocess.check_output(cmd, shell=True, text=True)
    assert "Compound Engineering activated" in out
    assert "Agent: compound" in out


@pytest.mark.integration
def test_router_preserves_existing_agents():
    router = ROOT / ".claude" / "hooks" / "router.sh"
    out_research = subprocess.check_output(
        f"bash {router} '/research q'", shell=True, text=True
    )
    out_synth = subprocess.check_output(
        f"bash {router} '/synthesize a b'", shell=True, text=True
    )
    assert "Research Agent activated" in out_research
    assert "Synthesis Agent activated" in out_synth

