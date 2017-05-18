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
    def __init__(self, ntbk):
        self.ntbk = _check_nb_file(ntbk)
        self.preprocessors = []

    def __repr__(self):
        s = "Number of preprocessors: {}\n---".format(
            len(self.preprocessors))
        for pre in self.preprocessors:
            s += '\n' + str(pre)
        return s

    def clear(self, output=False, content=False, stderr=False, tag=None):
        """Clear the components of a notebook cell.

        Parameters
        ----------
        output : bool
            Whether to clear the output of cells.
        content : bool
            Whether to clear the content of cells.
        stderr : bool
            Whether to clear the stderr of cells.
        tag : string | None
            Only apply clearing to cells with a certain tag.
        """
        if not any([output, content, stderr]):
            raise ValueError("At least of the clear options must be True.")
        # See if the cell matches the string
        pre = ClearCells(output=output, content=content,
                         stderr=stderr, tag=str(tag))
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
        return self

    def remove_cells(self, tag):
        """Remove cells that contain a specific string.

        Parameters
        ----------
        match_text : str
            A string to search for in input cells. Any cells with the
            `match_text` inside will be removed.
        """
        # See if the cell matches the string
        pre = RemoveCells(tag=tag)
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
        print('Saving to {}'.format(path_save))
        if not os.path.isdir(dir_save):
            os.makedirs(dir_save)
        nbf.write(self.ntbk, path_save)
