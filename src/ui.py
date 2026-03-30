from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

class AssistantUI:
    def __init__(self):
        self.console = Console(width=100)

    def display_error(self, message: str):
        self.console.rule(f"[bold red]{message}[/bold red]")

    def display_good(self, message: str):
        self.console.print(f"{message}",style="green")

    def display_request(self, message: str):
        self.console.print(f"[bold yellow]{message}[/bold yellow]")

    def display(self, message: str):
        self.console.print(f"{message}")

    def display_ai_response(self, text: str):
        self.console.print(Panel(Markdown(text), title="Aether AI", border_style="blue"))
