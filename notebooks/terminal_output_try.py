from rich.console import Console
from rich.progress import track
from pyfiglet import Figlet
import time

console = Console()
console.print(Figlet(font='slant').renderText('QuietEye'), style="cyan")

console.rule("[bold green]System Startup[/bold green]")
console.log("Camera Initialized")
console.log("Face detection model loaded")

for _ in track(range(5), description="Analyzing..."):
    time.sleep(1)

console.rule("[bold magenta]Done[/bold magenta]")
