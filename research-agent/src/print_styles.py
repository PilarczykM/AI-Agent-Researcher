from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()


def get_user_input(prompt_text="You"):
    """Get user input with styled prompt."""
    return Prompt.ask(f"[bold green]\n{prompt_text}[/bold green]")


def print_agent_response(response, title="Agent"):
    """Print the AI response in a styled panel."""
    panel = Panel(
        Text(response, style="cyan"),
        title=f"[bold blue]{title}[/bold blue]",
        expand=False,
    )
    console.print(panel)


def print_info(message):
    """Display an informational message."""
    console.print(f"[bold blue][INFO][/bold blue] {message}")


def print_error(message):
    """Display an error message."""
    console.print(f"[bold red][ERROR][/bold red] {message}")
