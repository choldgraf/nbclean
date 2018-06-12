import nbclean as nbc
import pytest
import os

# We'll use the test notebook in `examples`
path = os.path.dirname(__file__)
path_notebook = path + '/../../examples/test_notebooks/test_notebook.ipynb'
HIDE_TEXT = '# HIDDEN'

# Clear different parts of the notebook cells based on tags
ntbk = nbc.NotebookCleaner(path_notebook)
ntbk.clear(kind='output', tag='hide_output')
ntbk.clear(kind='content', tag='hide_content')
ntbk.clear(kind=['stderr'], tag='hide_stderr')

with pytest.raises(ValueError):
    ntbk.clear(kind='foo')
with pytest.raises(ValueError):
    ntbk.clear(kind=[])

# Removing entire cells
ntbk.remove_cells(tag='remove')
ntbk.remove_cells(tag='remove_if_empty', empty=True)
ntbk.remove_cells(search_text=HIDE_TEXT)

# Replacing text
text_replace_begin = '### SOLUTION BEGIN'
text_replace_end = '### SOLUTION END'
ntbk.replace_text(text_replace_begin, text_replace_end)


def test_nbclean():
    # Make sure we're testing for all of these
    TEST_KINDS = ['hide_output', 'hide_content', 'hide_stderr']
    for kind in TEST_KINDS:
        assert any(kind in cell['metadata'].get('tags', [])
                   for cell in ntbk.ntbk.cells)

    for cell in ntbk.ntbk.cells:
        # Tag removal
        tags = cell['metadata'].get('tags', None)
        if tags is None:
            continue
        if 'hide_output' in tags:
            assert len(cell['outputs']) == 0
        if 'hide_content' in tags:
            assert len(cell['source']) == 0
        if 'hide_stderr' in tags:
            assert all('stderr' != output.get('name', '')
                       for output in cell['outputs'])
        if 'remove_if_empty' in tags:
            assert len(cell['source']) != 0
        assert 'remove' not in tags
        assert HIDE_TEXT not in cell['source']

        # Text replacing
        if "# First we'll create 'a'" in cell['source']:
            assert '### SOLUTION BEGIN' not in cell['source']

    # Make sure final cell has all this stuff
    cell = ntbk.ntbk.cells[-1]
    assert len(cell['outputs']) != 0
    assert any('stderr' == output.get('name', '') for output in cell['outputs'])
    assert len(cell['source']) != 0

if __name__ == '__main__':
    test_nbclean()
