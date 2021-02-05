from subprocess import run
from pathlib import Path
from . import __path__ as dx_dir

__all__ = ["backup_pickles", "delete_backup_pickles"]

def run_shell_script(script_filename):
    """
    Run a shell script that sits in the same directory
    """
    sh_file = Path(dx_dir[0]) / script_filename
    if not sh_file.exists():
        raise FileNotFoundError(f"{sh_file} is missing")
    run(["sh", sh_file])

def backup_pickles(backup_script="backup_pickles.sh"):
    run_shell_script(backup_script)

def delete_backup_pickles(backup_script="remove_backup_pickles.sh"):
    run_shell_script(backup_script)
