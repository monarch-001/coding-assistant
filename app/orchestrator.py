import asyncio
from typing import List, Dict, Any
from .agents import architect, developer, reviewer, analyzer
from rich.console import Console

console = Console()

async def sequential_workflow(task: str) -> str:
    """Demonstrates a Sequential Workflow: Architect -> Developer."""
    console.print("[bold blue]Phase 1: Architecting solution...[/bold blue]")
    plan = await architect.run(f"Create a plan for this task: {task}")
    console.print("[green]Architect's Plan received.[/green]")
    
    console.print("[bold blue]Phase 2: Developing code...[/bold blue]")
    code = await developer.run(f"Implement this plan: {plan}")
    console.print("[green]Implementation complete.[/green]")
    
    return f"PLAN:\n{plan}\n\nIMPLEMENTATION:\n{code}"

async def loop_workflow(task: str, max_retries: int = 3) -> str:
    """Demonstrates a Loop Workflow: Developer <-> Reviewer."""
    console.print("[bold blue]Starting Refinement Loop...[/bold blue]")
    
    current_task = task
    for i in range(max_retries):
        console.print(f"[yellow]Iteration {i+1}: Implementing/Refactoring...[/yellow]")
        code = await developer.run(current_task)
        
        console.print(f"[yellow]Iteration {i+1}: Reviewing...[/yellow]")
        review = await reviewer.run(f"Review this code: {code}")
        
        if "APPROVED" in review.upper():
            console.print("[bold green]Code approved by Reviewer![/bold green]")
            return code
        
        console.print("[red]Reviewer requested changes. Looping back to Developer...[/red]")
        current_task = f"Fix these issues found in review: {review}\n\nOriginal Task: {task}\n\nCurrent Code: {code}"
        
    console.print("[bold red]Max retries reached without approval.[/bold red]")
    return f"Final version (not fully approved):\n{code}"

async def parallel_workflow(files: List[str]) -> Dict[str, str]:
    """Demonstrates a Parallel Workflow: Analyzing multiple files concurrently."""
    console.print(f"[bold blue]Starting Parallel Analysis on {len(files)} files...[/bold blue]")
    
    tasks = [analyzer.run(f"Analyze the complexity and health of {f}") for f in files]
    results = await asyncio.gather(*tasks)
    
    analysis_report = {}
    for file, report in zip(files, results):
        analysis_report[file] = report
        console.print(f"[green]Analysis complete for {file}[/green]")
        
    return analysis_report
