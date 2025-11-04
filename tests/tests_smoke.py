import subprocess
import sys
from importlib import import_module


def test_package_imports():
    mod = import_module("invoicegen")
    assert hasattr(mod, "__version__")


def test_cli_help_exits_zero_and_shows_usage():
    proc = subprocess.run(
        [sys.executable, "-m", "invoicegen", "--help"],
        check=False, capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "usage" in proc.stdout.lower()
