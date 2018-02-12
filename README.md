# nbclean
A collection of tools to preprocess, modify, and otherwise clean up Jupyter Notebooks.

<img src="doc/_static/images/demo.png" width=700px />


## Installation
You can install `nbclean` with pip:

```bash
pip install nbclean
```

## Usage

You can use `nbclean` to "clean up" Jupyter notebooks, including:

* Clear cell outputs, cell content, or components of cell outputs.
* Replace text in cells with new text of your choosing.
* Filter the above operations by the presence of **cell tags**.

The primary feature of `nbclean` is the `NotebookCleaner` class, which performs
the above actions on a notebook according to tags that are in each cell's
metadata.

See the [sample teacher notebook](examples/test_notebooks/test_notebook.ipynb) and
corresponding [nbclean notebook that modifies it](examples/modify_notebooks.ipynb).

Additionally, you can give it a try yourself by clicking the Binder button below:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/choldgraf/nbclean/master?filepath=examples%2Fmodify_notebooks.ipynb)