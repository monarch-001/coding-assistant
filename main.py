import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from app.router import RouterAgent
import sys

console = Console()

async def main():
    console.print(Panel.fit(
        "[bold cyan]Multi-Agent AI Coding Assistant[/bold cyan]\n"
        "[dim]Demonstrating Google ADK: Router, Sequential, Parallel, Loop, Memory, and Tools[/dim]",
        border_style="cyan"
    ))
    
    router = RouterAgent()
    await router.initialize()
    
    console.print(f"[dim]Session initialized with Thread ID: {router.thread_id}[/dim]\n")
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold green]You[/bold green]")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[yellow]Exiting. Happy coding![/yellow]")
                break
            
            if not user_input.strip():
                continue
                
            with console.status("[bold blue]Agents are collaborating...[/bold blue]", spinner="dots"):
                response = await router.chat(user_input)
            
            console.print("\n[bold cyan]Assistant[/bold cyan]")
            console.print(Markdown(response))
            console.print("-" * 20)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user. Exiting...[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
