import click
import nbformat as nbf
from glob import glob
from .clean import NotebookCleaner
from .run import run_notebook

@click.group()
def main():
    """Command-line tools for cleaning notebooks."""
    pass

@main.command()
@click.argument("pattern")
@click.option("--kind", default="output", help="What element of the notebooks you wish to clear")
def clear(pattern, kind="output", **kwargs):
    notebooks = glob(pattern, recursive=True)
    for path in notebooks:
        cleaner = NotebookCleaner(path)
        cleaner.clear(kind, **kwargs)
        cleaner.save(path)


@main.command()
@click.argument("pattern")
@click.option("--max_output_lines", default=1000, help="The maximum number of lines allowed in notebook outputs.")
def run(pattern, max_output_lines=1000, **kwargs):
    notebooks = glob(pattern, recursive=True)
    for path in notebooks:
        print(f"Running {path}")
        ntbk = run_notebook(path, max_output_lines=max_output_lines)
        nbf.write(ntbk, path)
