import nbformat as nbf
import os
import os.path as op
from nbgrader.preprocessors import LimitOutput, Execute
from .utils import _check_nb_file
from glob import glob
from tqdm import tqdm


def run_notebook_directory(path, path_save=None, max_output_lines=1000,
                           overwrite=False):
    """Run all the notebooks in a directory and save them somewhere else.

    Parameters
    ----------
    path : str
        A path to a directory that contains jupyter notebooks.
        All notebooks in this folder ending in `.ipynb` will be run,
        and the outputs will be placed in `path_save`. This may
        optionally contain a wildcard matching ``<something>.ipynb`` in which
        case only notebooks that match will be run.
    path_save : str | None
        A path to a directory to save the notebooks. If this doesn't exist,
        it will be created. If `None`, notebooks will not be saved.
    max_output_lines : int | None
        The maximum number of lines allowed in notebook outputs.
    overwrite : bool
        Whether to overwrite the output directory if it exists.

    Returns
    -------
    notebooks : list
        A list of the `NotebookNode` instances, one for each notebook.
    """
    if not op.exists(path):
        raise ValueError("You've specified an input path that doesn't exist")
    to_glob = op.join(path, '*.ipynb') if '.ipynb' not in path else path
    notebooks = glob(to_glob)

    # Execute notebooks
    outputs = []
    for notebook in tqdm(notebooks):
        outputs.append(run_notebook(notebook,
                                    max_output_lines=max_output_lines))

    # Now save them
    if path_save is not None:
        print('Saving {} notebooks to: {}'.format(len(notebooks), path_save))
        if not op.exists(path_save):
            os.makedirs(path_save)
        elif overwrite is True:
            print('Overwriting output directory')
            for ifile in glob(path_save + '*-exe.ipynb'):
                os.remove(ifile)
        else:
            raise ValueError('path_save exists and overwrite is not True')

        for filename, notebook in zip(notebooks, outputs):
            this_name = op.basename(filename)
            left, right = this_name.split('.')
            left += '-exe'
            this_name = '.'.join([left, right])
            nbf.write(notebook, op.join(path_save, this_name))


def run_notebook(ntbk, max_output_lines=1000):
    """Run the cells in a notebook and limit the output length.

    Parameters
    ----------
    ntbk : string | instance of NotebookNode
        The input notebook.
    max_output_lines : int | None
        The maximum number of lines allowed in notebook outputs.
    """
    ntbk = _check_nb_file(ntbk)

    preprocessors = [Execute()]
    if max_output_lines is not None:
        preprocessors.append(LimitOutput(max_lines=max_output_lines,
                                         max_traceback=max_output_lines))
    for prep in preprocessors:
        ntbk, _ = prep.preprocess(ntbk, {})
    return ntbk
