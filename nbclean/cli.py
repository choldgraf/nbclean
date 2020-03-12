import click
import nbformat as nbf
from glob import glob
from nbclient import execute
from .clean import NotebookCleaner
from .run import run_notebook

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

def _find_notebooks(path, skip):
    from pathlib import Path
    path = Path(path)
    if not path.exists():
        raise ValueError(f"You gave a path that doesn't exist: {path}")
    elif path.is_dir():
        notebooks = list(path.rglob("*.ipynb"))
        notebooks = [ii for ii in notebooks if skip not in str(ii)]
    elif path.suffix == ".ipynb":
        notebooks = [str(path)]
    else:
        raise ValueError(f"You gave a path that isn't a folder or a notebook file: {path}")
    return notebooks

def clear_notebooks(path, kind, skip=".ipynb_checkpoints", **kwargs):
    notebooks = _find_notebooks(path, skip)
    if len(notebooks) == 0:
        print("Note: no notebooks were found to be cleared.")
    for path in notebooks:
        print(f"Clearing {kind} in {path}")
        cleaner = NotebookCleaner(str(path))
        cleaner.clear(kind, **kwargs)
        cleaner.save(str(path))


@main.command()
@click.argument("path")
@click.option("--skip", default=".ipynb_checkpoints", help="What element of the notebooks you wish to clear")
def run(path, skip, **kwargs):
    run_notebooks(path, skip, **kwargs)

def run_notebooks(path, skip, **kwargs):
    notebooks = _find_notebooks(path, skip)
    if len(notebooks) == 0:
        print("Note: no notebooks were found to be executed.")

    for path in notebooks:
        print(f"Running {path}")
        ntbk = nbf.read(str(path), nbf.NO_CONVERT)
        ntbk = execute(ntbk, cwd=str(path.parent))
        nbf.write(ntbk, str(path))