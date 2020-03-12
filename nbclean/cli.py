import click
import nbformat as nbf
from glob import glob
from .clean import clear_notebooks
from .run import run_notebooks

@click.group()
def main():
    """Command-line tools for cleaning notebooks."""
    pass

@main.command()
@click.argument("path")
@click.option("--kind", default="output", help="What element of the notebooks you wish to clear")
@click.option("--skip", default=".ipynb_checkpoints", help="What element of the notebooks you wish to clear")
def clear(path, kind, skip, **kwargs):
    clear_notebooks(path, kind, skip=skip, **kwargs)

@main.command()
@click.argument("path")
@click.option("--skip", default=".ipynb_checkpoints", help="What element of the notebooks you wish to clear")
def run(path, skip, **kwargs):
    run_notebooks(path, skip, **kwargs)
