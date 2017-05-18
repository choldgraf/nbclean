import nbformat as nbf
from nbformat.notebooknode import NotebookNode
from copy import deepcopy


def _check_nb_file(ntbk):
    if isinstance(ntbk, str):
        ntbk = nbf.read(ntbk, nbf.NO_CONVERT)
    elif not isinstance(ntbk, NotebookNode):
        raise TypeError('`ntbk` must be type string or `NotebookNode`')
    ntbk = deepcopy(ntbk)
    return ntbk
