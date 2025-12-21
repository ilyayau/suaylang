import shutil
import sys
import subprocess

def test_suay_cli_exists():
    exe = shutil.which("suay")
    assert exe is not None or hasattr(sys.modules, "suaylang.cli"), "suay CLI not found and no module fallback"
    out = subprocess.run([exe or sys.executable, *("-m", "suaylang.cli") if exe is None else (), "--help"], capture_output=True, text=True)
    assert out.returncode == 0
    assert "SuayLang CLI" in out.stdout or "usage" in out.stdout

def test_suay_vm_cli_exists():
    exe = shutil.which("suay-vm")
    assert exe is not None or hasattr(sys.modules, "suaylang.vm_cli"), "suay-vm CLI not found and no module fallback"
    out = subprocess.run([exe or sys.executable, *("-m", "suaylang.vm_cli") if exe is None else (), "--help"], capture_output=True, text=True)
    assert out.returncode == 0
    assert "SuayLang VM CLI" in out.stdout or "usage" in out.stdout
