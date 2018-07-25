import hashlib
import os

from traitlets import Unicode, Bool
from nbgrader.preprocessors import NbGraderPreprocessor


class RemoveCells(NbGraderPreprocessor):
    """A helper class to remove cells from a notebook.

    This should not be used directly, instead, use the
    NotebookCleaner class.
    """

    tag = Unicode("None")
    tag = Unicode("None")
    empty = Bool(False)

    def preprocess(self, nb, resources):
        if self.tag == 'None' and self.empty is False and self.search_text == 'None':
            raise ValueError("One of `tag`, `empty`, or `search_text` must be used.")
        new_cells = []
        for ii, cell in enumerate(nb['cells']):
            is_empty = len(cell['source']) == 0
            if self.tag != 'None':
                if self.tag in cell['metadata'].get('tags', []):
                    # Skip appending the cell if the tag matches
                    if self.empty:
                        if is_empty:
                            continue
                    else:
                        continue
            elif self.search_text != 'None':
                if self.search_text in cell['source']:
                    # Skip appending the cell if the tag matches
                    if self.empty:
                        if is_empty:
                            continue
                    else:
                        continue
            elif self.empty and is_empty:
                continue
            # If we didn't trigger anything above, append the cell to keep it
            new_cells.append(cell)
        nb['cells'] = new_cells
        return nb, resources

    def __repr__(self):
        s = "<RemoveCells> Tag: {}".format(self.tag)
        if self.empty:
            s += ' | Remove if empty'
        return s


class ConvertCells:
    """A helper class to convert cells in a notebook to oktests.

    This should not be used directly, instead, use the
    NotebookCleaner class.
    """

    template = '''
test = {
  'name': 'test_valid',
  'points': 1,
  'suites': [
    {
      'cases': [{'code': r"""
%s
      """},
      ]
    }
  ]
}
'''

    def __init__(self, tag, oktest_path, notebook_dir):
        self.tag = tag
        # path relative to the output notebook
        self.oktest_path = oktest_path
        # path to the notebook
        self.notebook_dir = notebook_dir

    def preprocess(self, nb, resources):
        os.makedirs(self.oktest_path, exist_ok=True)

        new_cells = []
        for cell in nb['cells']:
            cell_tags = cell['metadata'].get('tags', [])
            if self.tag in cell_tags:
                # convert cell
                source = cell['source']
                print(source)
                h = hashlib.md5(source.encode('utf-8')).hexdigest()[:7]
                oktest = os.path.join(self.oktest_path, 'q-%s.py' % h)
                with open(os.path.join(self.notebook_dir, oktest), 'w') as f:
                    lines = ["      >>> " + l for l in source.split("\n") if l]
                    f.write(self.template % '\n'.join(lines))

                cell['source'] = 'check("%s")' % oktest
                new_cells.append(cell)

            else:
                new_cells.append(cell)

        nb['cells'] = new_cells
        return nb, resources

    def __repr__(self):
        s = "<ConvertCells> Tag: {}".format(self.tag)
        return s


class ClearCells(NbGraderPreprocessor):
    """A helper class to remove cells from a notebook.

    This should not be used directly, instead, use the
    NotebookCleaner class.
    """

    output = Bool(True)
    output_image = Bool(False)
    output_text = Bool(False)
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

            # Clear all cell output
            if self.output is True:
                if 'outputs' in cell.keys():
                    cell['outputs'] = []

            # Clear cell text output
            if self.output_text is True:
                if 'outputs' in cell.keys():
                    for output in cell['outputs']:
                        data = output.get('data', {})
                        for key in list(data.keys()):
                            if 'text/' in key:
                                data.pop(key)

            # Clear cell image output
            if self.output_image is True:
                if 'outputs' in cell.keys():
                    for output in cell['outputs']:
                        data = output.get('data', {})
                        for key in list(data.keys()):
                            if 'image/' in key:
                                data.pop(key)

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
