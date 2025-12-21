import shutil
import sys
import subprocess

def test_suay_cli_exists():
    exe = shutil.which("suay")
    assert exe is not None or hasattr(sys.modules, "suaylang.cli"), "suay CLI not found and no module fallback"
    if exe is not None:
        cmd = [exe, "--help"]
    else:
        cmd = [sys.executable, "-m", "suaylang.cli", "--help"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    assert out.returncode == 0
    assert "SuayLang CLI" in out.stdout or "usage" in out.stdout

def test_suay_vm_cli_exists():
    exe = shutil.which("suay-vm")
    assert exe is not None or hasattr(sys.modules, "suaylang.vm_cli"), "suay-vm CLI not found and no module fallback"
    if exe is not None:
        cmd = [exe, "--help"]
    else:
        cmd = [sys.executable, "-m", "suaylang.vm_cli", "--help"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    assert out.returncode == 0
    assert "SuayLang VM CLI" in out.stdout or "usage" in out.stdout
