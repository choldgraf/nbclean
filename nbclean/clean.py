"""Functions to assist with grading."""
import nbformat as nbf
import os
from nbgrader.preprocessors import ClearSolutions
from .preprocessors import RemoveCells, ClearCells
from .utils import _check_nb_file


class NotebookCleaner(object):
    """Prepare Jupyter notebooks for distribution to students.

    Parameters
    ----------
    ntbk : string | instance of NotebookNode
        The input notebook.
    """
    def __init__(self, ntbk, verbose=False):
        self._verbose = verbose
        self.ntbk = _check_nb_file(ntbk)
        self.preprocessors = []

    def __repr__(self):
        s = "Number of preprocessors: {}\n---".format(
            len(self.preprocessors))
        for pre in self.preprocessors:
            s += '\n' + str(pre)
        return s

    def clear(self, kind, tag=None):
        """Clear the components of a notebook cell.

        Parameters
        ----------
        kind : string | list of strings
            The elements of the notebook you wish to clear. Must be one of:
                "content": the content of cells.
                "output": the entire output of cells.
                "output_text": the text output of cells.
                "output_image": the image output of cells.
                "stderr": the stderr of cells.
            If a list, must contain one or more of the above strings.
        tag : string | None
            Only apply clearing to cells with a certain tag. If
            None, apply clearing to all cells.
        """
        ALLOWED_KINDS = ['content', 'output', 'output_text',
                         'output_image', 'stderr']
        if isinstance(kind, str):
            kind = [kind]
        if not isinstance(kind, list) or len(kind) == 0:
            raise ValueError('kind must be a list of at least one string. All '
                             'strings must be one of {}'.format(ALLOWED_KINDS))
        if any(ii not in ALLOWED_KINDS for ii in kind):
            raise ValueError('Unknown kind found. kind must be one of {}'.format(ALLOWED_KINDS))
        kwargs = {key: key in kind for key in ALLOWED_KINDS}

        # See if the cell matches the string
        pre = ClearCells(tag=str(tag), **kwargs)
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
        return self

    def remove_cells(self, tag=None, empty=False, search_text=None):
        """Remove cells that match a given tag.

        Parameters
        ----------
        tag : str | None
            A string to search for in cell tags cells. Any cells with the
            tag inside will be removed.
        empty : bool
            Whether to remove any cell that is empty.
        search_text : str | None
            A string to search for within cells. Any cells with this string
            inside will be removed.
        """
        # See if the cell matches the string
        tag = 'None' if tag is None else tag
        search_text = 'None' if search_text is None else search_text

        pre = RemoveCells(tag=tag, empty=empty, search_text=search_text)
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
        return self

    def replace_text(self, text_replace_begin=u'### SOLUTION BEGIN',
                     text_replace_end=u'### SOLUTION END',
                     replace_code=None, replace_md=None):
        """Create answer cells for students to fill out.

        This will remove all text after `match_string`. Students should then
        give their answers in this section. Alternatively, a markdown cell will
        replace the student answer cell

        Parameters
        ----------
        text_replace_begin : str
            A string to search for in input cells. If the string is
            found, then anything between it and `text_replace_end` is removed.
        text_replace_end : str
            The ending delimiter for solution cells.
        replace_code : str | None
            Text to add to code solution cells. If None, `nbgrader`
            default is used.
        replace_md : str | None
            Text to add to markdown solution cells. If None, a default template
            will be used.
        """
        kwargs = dict(begin_solution_delimeter=text_replace_begin,
                      end_solution_delimeter=text_replace_end,
                      enforce_metadata=False)
        if replace_code is not None:
            kwargs['code_stub'] = dict(python=replace_code)
        if replace_md is None:
            replace_md = ('---\n## <span style="color:red">Student Answer</span>'
                          '\n\n*Double-click and add your answer between the '
                          'lines*\n\n---')
        kwargs['text_stub'] = replace_md
        pre = ClearSolutions(**kwargs)
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
        return self

    def save(self, path_save):
        """Save the notebook to disk.

        Parameters
        ----------
        path_save : string
            The path for saving the file.
        """
        dir_save = os.path.dirname(path_save)
        if self._verbose is True:
            print('Saving to {}'.format(path_save))
        if not os.path.isdir(dir_save):
            os.makedirs(dir_save)
        nbf.write(self.ntbk, path_save)
