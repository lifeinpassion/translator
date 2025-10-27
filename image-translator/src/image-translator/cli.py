"""
Command-line interface for image translator.
"""

import logging
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.progress import track
import yaml

from .core.pipeline import TranslationPipeline
from .batch.batch_processor import BatchProcessor
from .utils.logging_config import setup_logging
from .utils.config import load_config

app = typer.Typer(
    name="imgtrans",
    help="Production-ready image translation for English ↔ Chinese on macOS",
    add_completion=True,
)
console = Console()


@app.callback()
def callback(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file",
        exists=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
):
    """Global options."""
    level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=level)
    
    # Load configuration
    if config:
        ctx.obj = load_config(config)
    else:
        # Load default config
        default_config = Path(__file__).parent.parent.parent / "config" / "default_config.yaml"
        ctx.obj = load_config(default_config)


@app.command()
def translate(
    ctx: typer.Context,
    input_file: Path = typer.Argument(..., help="Input image file", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    visualize: bool = typer.Option(False, "--viz", help="Draw bounding boxes"),
):
    """Translate text in a single image."""
    try:
        console.print(f"[bold blue]Translating:[/bold blue] {input_file}")
        
        # Initialize pipeline
        pipeline = TranslationPipeline(ctx.obj)
        
        # Generate output path if not provided
        if not output:
            output = input_file.parent / f"{input_file.stem}_translated{input_file.suffix}"
        
        # Translate
        pipeline.translate_image(str(input_file), str(output), visualize)
        
        console.print(f"[bold green]✓[/bold green] Saved to: {output}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def batch(
    ctx: typer.Context,
    input_dir: Path = typer.Argument(..., help="Input directory", exists=True),
    output_dir: Path = typer.Argument(..., help="Output directory"),
    pattern: str = typer.Option("*.png,*.jpg,*.jpeg", "--pattern", "-p", help="File patterns"),
    workers: int = typer.Option(4, "--workers", "-w", help="Number of parallel workers"),
):
    """Batch process multiple images."""
    try:
        console.print(f"[bold blue]Batch processing:[/bold blue] {input_dir}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Collect files
        patterns = pattern.split(',')
        files = []
        for pat in patterns:
            files.extend(input_dir.glob(pat))
        
        if not files:
            console.print("[yellow]No files found![/yellow]")
            return
        
        console.print(f"Found {len(files)} images")
        
        # Process batch
        processor = BatchProcessor(ctx.obj, num_workers=workers)
        results = processor.process_batch(
            [str(f) for f in files],
            str(output_dir)
        )
        
        # Summary
        success_count = len(results['successes'])
        failure_count = len(results['failures'])
        
        console.print(f"[bold green]✓ Completed:[/bold green] {success_count}/{len(files)}")
        if failure_count > 0:
            console.print(f"[bold red]✗ Failed:[/bold red] {failure_count}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def pdf(
    ctx: typer.Context,
    input_file: Path = typer.Argument(..., help="Input PDF file", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output PDF path"),
):
    """Translate text in PDF document."""
    console.print("[yellow]PDF translation coming soon![/yellow]")
    # TODO: Implement PDF translation


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()