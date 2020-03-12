import nbformat as nbf
import os
import os.path as op
from nbgrader.preprocessors import LimitOutput, Execute
from .utils import _check_nb_file, _find_notebooks
from glob import glob
from pathlib import Path
from tqdm import tqdm
from nbclient import execute


def run_notebooks(path, skip, **kwargs):
    notebooks = _find_notebooks(path, skip)
    if len(notebooks) == 0:
        print("Note: no notebooks were found to be executed.")

    for path in notebooks:
        print(f"Running {path}")
        ntbk = run_notebook(path)
        nbf.write(ntbk, str(path))


def run_notebook(ntbk, max_output_lines=1000):
    """Run the cells in a notebook and limit the output length.

    Parameters
    ----------
    ntbk : string | instance of NotebookNode
        The input notebook.
    max_output_lines : int | None
        The maximum number of lines allowed in notebook outputs.
    """
    if isinstance(ntbk, (str, type(Path))):
        ntbk = Path(ntbk)
        wd = str(ntbk.parent)
        ntbk = str(ntbk)
    else:
        wd = str(Path())
    ntbk = _check_nb_file(ntbk)
    ntbk = execute(ntbk, cwd=wd)
    return ntbk
