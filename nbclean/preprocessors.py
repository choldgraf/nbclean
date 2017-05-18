from traitlets import Unicode, Bool
from nbgrader.preprocessors import NbGraderPreprocessor


class RemoveCells(NbGraderPreprocessor):
    """A helper class to remove cells from a notebook.

    This should not be used directly, instead, use the
    NotebookCleaner class.
    """

    tag = Unicode("None")

    def preprocess(self, nb, resources):

        new_cells = []
        for ii, cell in enumerate(nb['cells']):
            if self.tag != 'None':
                tags = cell['metadata'].get('tags', [])
                # Only keep the cell if the tag doesn't match
                if self.tag not in tags:
                    new_cells.append(cell)
        nb['cells'] = new_cells
        return nb, resources


class ClearCells(NbGraderPreprocessor):
    """A helper class to remove cells from a notebook.

    This should not be used directly, instead, use the
    NotebookCleaner class.
    """

    output = Bool(True)
    content = Bool(False)
    stderr = Bool(True)
    tag = Unicode('None')

    def preprocess(self, nb, resources):
        for cell in nb['cells']:
            # Check to see whether we process this cell
            if self.tag != 'None':
                tags = cell['metadata'].get('tags', [])
                if self.tag not in tags:
                    continue

            # Clear cell output
            if self.output is True:
                if 'outputs' in cell.keys():
                    cell['outputs'] = []

            # Clear cell content
            if self.content is True:
                cell['source'] = ''

            # Clear stdout
            if self.stderr is True:
                new_outputs = []
                if 'outputs' not in cell.keys():
                    continue
                for output in cell['outputs']:
                    name = output.get('name', None)
                    if name != 'stderr':
                        new_outputs.append(output)
                cell['outputs'] = new_outputs

        return nb, resources

    def __repr__(self):
        s = "<ClearCells> Tag: {}".format(self.tag)
        return s
