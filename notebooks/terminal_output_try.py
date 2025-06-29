from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from pyfiglet import Figlet
import time
import random

console = Console()

def startup_sequence():
    # Clear screen and show main title
    console.clear()
    
    # Create stylized title with gradient effect
    title_text = Text(Figlet(font='slant').renderText('QuietEye'), style="bold cyan")
    subtitle = Text("Advanced Surveillance & Detection System", style="italic dim white")
    version = Text("v2.1.4-alpha | Build 20250628", style="dim yellow")
    
    # Main title panel
    title_panel = Panel(
        Align.center(title_text + "\n" + subtitle + "\n" + version),
        border_style="bright_cyan",
        padding=(1, 2),
        title="[bold white]⚡ SYSTEM INITIALIZATION ⚡[/bold white]",
        title_align="center"
    )
    
    console.print(title_panel)
    console.print()
    
    # System info table
    sys_table = Table(show_header=False, box=None, padding=(0, 2))
    sys_table.add_row("[cyan]⚙️  Architecture:[/cyan]", "[white]x86_64[/white]")
    sys_table.add_row("[cyan]🖥️  Platform:[/cyan]", "[white]Linux 5.15.0-LTS[/white]")
    sys_table.add_row("[cyan]🔧  Python:[/cyan]", "[white]3.11.2[/white]")
    sys_table.add_row("[cyan]🎯  Mode:[/cyan]", "[bold green]STEALTH[/bold green]")
    
    console.print(Panel(sys_table, title="[bold blue]System Information[/bold blue]", border_style="blue"))
    console.print()
    
    # Startup sequence with enhanced progress bars
    startup_tasks = [
        ("🔌 Initializing hardware interfaces", 0.8, "green"),
        ("📷 Loading camera modules", 1.2, "cyan"),
        ("🧠 Loading AI detection models", 2.0, "magenta"),
        ("🔍 Calibrating facial recognition", 1.5, "yellow"),
        ("🛡️  Activating security protocols", 1.0, "red"),
        ("🌐 Establishing network connections", 0.9, "blue"),
        ("✅ System ready - All modules online", 0.5, "bright_green")
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        
        for task_desc, duration, color in startup_tasks:
            task = progress.add_task(f"[{color}]{task_desc}[/{color}]", total=100)
            
            # Simulate realistic loading with variable speeds
            for i in range(100):
                progress.update(task, advance=1)
                # Add some randomness to make it feel more realistic
                delay = (duration / 100) + random.uniform(-0.005, 0.01)
                time.sleep(max(0.01, delay))
    
    console.print()
    
    # System status dashboard
    status_table = Table(show_header=True, header_style="bold white", box=None)
    status_table.add_column("Component", style="cyan", width=25)
    status_table.add_column("Status", width=15, justify="center")
    status_table.add_column("Performance", width=15, justify="center")
    
    components = [
        ("Camera Feed", "[bold green]●[/bold green] ACTIVE", "[green]98.7%[/green]"),
        ("Face Detection", "[bold green]●[/bold green] ONLINE", "[green]99.2%[/green]"),
        ("Neural Network", "[bold green]●[/bold green] READY", "[green]97.8%[/green]"),
        ("Security Layer", "[bold green]●[/bold green] ARMED", "[green]100%[/green]"),
        ("Data Pipeline", "[bold green]●[/bold green] FLOWING", "[green]95.4%[/green]")
    ]
    
    for comp, status, perf in components:
        status_table.add_row(f"🔧 {comp}", status, perf)
    
    console.print(Panel(
        status_table,
        title="[bold green]🎯 SYSTEM STATUS DASHBOARD[/bold green]",
        border_style="bright_green",
        padding=(1, 2)
    ))
    
    console.print()
    
    # Final success message
    success_panel = Panel(
        Align.center(
            Text("🚀 QUIETEYE SYSTEM FULLY OPERATIONAL 🚀", style="bold bright_green") + 
            Text("\n\nAll subsystems initialized successfully\nReady for surveillance operations", style="dim white")
        ),
        border_style="bright_green",
        padding=(1, 2)
    )
    
    console.print(success_panel)
    
    # Add some final flair
    console.print("\n" + "═" * 70, style="dim cyan")
    console.print("🕵️  Monitoring initiated - Stay vigilant", style="bold cyan", justify="center")
    console.print("═" * 70 + "\n", style="dim cyan")

if __name__ == "__main__":
    startup_sequence()