import subprocess
import sys

from rich.console import Console

console = Console()


def main():
    """Run mypy and flake8 on the tracker package"""
    commands = [
        ["mypy", "tracker"],
        ["flake8", "tracker"],
    ]

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            console.print(
                    "[bold red]Command failed[/bold red]"
                    )
            sys.exit(1)

    console.print("[bold green]All checks passed![/bold green]")


if __name__ == "__main__":
    main()
