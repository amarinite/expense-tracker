import subprocess
import sys

from rich.console import Console

console = Console()

CHECKS = [
    [sys.executable, "-m", "mypy", "tracker"],
    [sys.executable, "-m", "flake8", "tracker"],
    [sys.executable, "-m", "pytest", "-q"],
]


def run_checks() -> bool:
    """Run all checks, stopping at the first failure"""
    for cmd in CHECKS:
        console.print(f"[bold]Running:[/bold] {' '.join(cmd[2:])}")
        if subprocess.run(cmd).returncode != 0:
            console.print("[bold red]Command failed[/bold red]")
            return False
    console.print("[bold green]All checks passed![/bold green]")
    return True


def check() -> int:
    """Checks only"""
    return 0 if run_checks() else 1


def run() -> int:
    """Checks, then the program, forwarding CLI arguments."""
    if not run_checks():
        return 1
    cmd = [sys.executable, "-m", "tracker", *sys.argv[1:]]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    sys.exit(check())
