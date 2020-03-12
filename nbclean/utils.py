import nbformat as nbf
from nbformat.notebooknode import NotebookNode
from copy import deepcopy
from pathlib import Path


def _check_nb_file(ntbk):
    if isinstance(ntbk, Path):
        ntbk = str(ntbk)
    if isinstance(ntbk, str):
        ntbk = nbf.read(ntbk, nbf.NO_CONVERT)
    elif not isinstance(ntbk, NotebookNode):
        raise TypeError(f'`ntbk` must be type string or `NotebookNode`, found: {type(ntbk)}')
    ntbk = deepcopy(ntbk)
    return ntbk


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