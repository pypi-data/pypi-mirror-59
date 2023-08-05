# -*- coding: utf-8 -*-

import os
from nbformat.v4.nbbase import new_notebook, new_code_cell, new_markdown_cell, new_raw_cell
from jupytext.compare import compare, compare_notebooks
import jupytext


def test_read_simple_file(script="""# ---
# title: Simple file
# ---

# %% [markdown]
# This is a markdown cell

# %% [md]
# This is also a markdown cell

# %% [raw]
# This is a raw cell

# %%% sub-cell title
# This is a sub-cell

# %%%% sub-sub-cell title
# This is a sub-sub-cell

# %% And now a code cell
1 + 2 + 3 + 4
5
6
# %%magic # this is a commented magic, not a cell

7
"""):
    nb = jupytext.reads(script, 'py:percent')
    compare_notebooks(new_notebook(cells=[
        new_raw_cell('---\ntitle: Simple file\n---'),
        new_markdown_cell('This is a markdown cell'),
        new_markdown_cell('This is also a markdown cell', metadata={'region_name': 'md'}),
        new_raw_cell('This is a raw cell'),
        new_code_cell('# This is a sub-cell', metadata={'title': 'sub-cell title', 'cell_depth': 1}),
        new_code_cell('# This is a sub-sub-cell', metadata={'title': 'sub-sub-cell title', 'cell_depth': 2}),
        new_code_cell('''1 + 2 + 3 + 4
5
6
%%magic # this is a commented magic, not a cell

7''', metadata={'title': 'And now a code cell'})]), nb)

    script2 = jupytext.writes(nb, 'py:percent')
    compare(script2, script)


def test_read_cell_with_metadata(
        script="""# %% a code cell with parameters {"tags": ["parameters"]}
a = 3
"""):
    nb = jupytext.reads(script, 'py:percent')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'code'
    assert nb.cells[0].source == 'a = 3'
    assert nb.cells[0].metadata == {
        'title': 'a code cell with parameters',
        'tags': ['parameters']}

    script2 = jupytext.writes(nb, 'py:percent')
    compare(script2, script)


def test_read_nbconvert_script(script="""
# coding: utf-8

# A markdown cell

# In[1]:


import pandas as pd

pd.options.display.max_rows = 6
pd.options.display.max_columns = 20


# Another markdown cell

# In[2]:


1 + 1


# Again, a markdown cell

# In[33]:


2 + 2


# <codecell>


3 + 3
"""):
    assert jupytext.formats.guess_format(script, '.py')[0] == 'percent'
    nb = jupytext.reads(script, '.py')
    assert len(nb.cells) == 5


def test_read_remove_blank_lines(script="""# %%
import pandas as pd

# %% Display a data frame
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]},
                  index=pd.Index(['x0', 'x1'], name='x'))
df

# %% Pandas plot {"tags": ["parameters"]}
df.plot(kind='bar')


# %% sample class
class MyClass:
    pass


# %% a function
def f(x):
    return 42 * x

"""):
    nb = jupytext.reads(script, 'py')
    assert len(nb.cells) == 5
    for i in range(5):
        assert nb.cells[i].cell_type == 'code'
        assert not nb.cells[i].source.startswith('\n')
        assert not nb.cells[i].source.endswith('\n')

    script2 = jupytext.writes(nb, 'py:percent')
    compare(script2, script)


def test_no_crash_on_square_bracket(script="""# %% In [2]
print('Hello')
"""):
    nb = jupytext.reads(script, 'py')
    script2 = jupytext.writes(nb, 'py:percent')
    compare(script2, script)


def test_nbconvert_cell(script="""# In[2]:
print('Hello')
"""):
    nb = jupytext.reads(script, 'py')
    script2 = jupytext.writes(nb, 'py:percent')
    expected = """# %%
print('Hello')
"""
    compare(script2, expected)


def test_nbformat_v3_nbpy_cell(script="""# <codecell>
print('Hello')
"""):
    nb = jupytext.reads(script, 'py')
    script2 = jupytext.writes(nb, 'py:percent')
    expected = """# %%
print('Hello')
"""
    compare(script2, expected)


def test_multiple_empty_cells():
    nb = new_notebook(cells=[new_code_cell(), new_code_cell(), new_code_cell()],
                      metadata={'jupytext': {'notebook_metadata_filter': '-all'}})
    text = jupytext.writes(nb, 'py:percent')
    expected = """# %%

# %%

# %%
"""
    compare(text, expected)
    nb2 = jupytext.reads(text, 'py:percent')
    nb2.metadata = nb.metadata
    compare(nb2, nb)


def test_first_cell_markdown_191():
    text = """# %% [markdown]
# Docstring

# %%
from math import pi

# %% [markdown]
# Another markdown cell
"""

    nb = jupytext.reads(text, 'py')
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[1].cell_type == 'code'
    assert nb.cells[2].cell_type == 'markdown'


def test_multiline_comments_in_markdown_1():
    text = """# %% [markdown]
'''
a
long
cell
'''
"""
    nb = jupytext.reads(text, 'py')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[0].source == "a\nlong\ncell"
    py = jupytext.writes(nb, 'py')
    compare(py, text)


def test_multiline_comments_in_markdown_2():
    text = '''# %% [markdown]
"""
a
long
cell
"""
'''
    nb = jupytext.reads(text, 'py')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[0].source == "a\nlong\ncell"
    py = jupytext.writes(nb, 'py')
    compare(py, text)


def test_multiline_comments_format_option():
    text = '''# %% [markdown]
"""
a
long
cell
"""
'''
    nb = new_notebook(cells=[new_markdown_cell("a\nlong\ncell")],
                      metadata={'jupytext': {'cell_markers': '"""',
                                             'notebook_metadata_filter': '-all'}})
    py = jupytext.writes(nb, 'py:percent')
    compare(py, text)


def test_multiline_comments_in_raw_cell():
    text = '''# %% [raw]
"""
some
text
"""
'''
    nb = jupytext.reads(text, 'py')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'raw'
    assert nb.cells[0].source == "some\ntext"
    py = jupytext.writes(nb, 'py')
    compare(py, text)


def test_multiline_comments_in_markdown_cell_no_line_return():
    text = '''# %% [markdown]
"""a
long
cell"""
'''
    nb = jupytext.reads(text, 'py')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[0].source == "a\nlong\ncell"


def test_multiline_comments_in_markdown_cell_is_robust_to_additional_cell_marker():
    text = '''# %% [markdown]
"""
some text, and a fake cell marker
# %% [raw]
"""
'''
    nb = jupytext.reads(text, 'py')
    assert len(nb.cells) == 1
    assert nb.cells[0].cell_type == 'markdown'
    assert nb.cells[0].source == "some text, and a fake cell marker\n# %% [raw]"
    py = jupytext.writes(nb, 'py')
    compare(py, text)


def test_cell_markers_option_in_contents_manager(tmpdir):
    tmp_ipynb = str(tmpdir.join('notebook.ipynb'))
    tmp_py = str(tmpdir.join('notebook.py'))

    cm = jupytext.TextFileContentsManager()
    cm.root_dir = str(tmpdir)

    nb = new_notebook(cells=[new_code_cell('1 + 1'), new_markdown_cell('a\nlong\ncell')],
                      metadata={'jupytext': {'formats': 'ipynb,py:percent',
                                             'notebook_metadata_filter': '-all',
                                             'cell_markers': "'''"}})
    cm.save(model=dict(type='notebook', content=nb), path='notebook.ipynb')

    assert os.path.isfile(tmp_ipynb)
    assert os.path.isfile(tmp_py)

    with open(tmp_py) as fp:
        text = fp.read()

    compare(text, """# %%
1 + 1

# %% [markdown]
'''
a
long
cell
'''
""")

    nb2 = jupytext.read(tmp_py)
    compare_notebooks(nb, nb2)


def test_default_cell_markers_in_contents_manager(tmpdir):
    tmp_ipynb = str(tmpdir.join('notebook.ipynb'))
    tmp_py = str(tmpdir.join('notebook.py'))

    cm = jupytext.TextFileContentsManager()
    cm.root_dir = str(tmpdir)
    cm.default_cell_markers = "'''"

    nb = new_notebook(cells=[new_code_cell('1 + 1'), new_markdown_cell('a\nlong\ncell')],
                      metadata={'jupytext': {'formats': 'ipynb,py:percent',
                                             'notebook_metadata_filter': '-all'}})
    cm.save(model=dict(type='notebook', content=nb), path='notebook.ipynb')

    assert os.path.isfile(tmp_ipynb)
    assert os.path.isfile(tmp_py)

    with open(tmp_py) as fp:
        text = fp.read()

    compare(text, """# %%
1 + 1

# %% [markdown]
'''
a
long
cell
'''
""")

    nb2 = jupytext.read(tmp_py)
    compare_notebooks(nb, nb2)


def test_default_cell_markers_in_contents_manager_does_not_impact_light_format(tmpdir):
    tmp_ipynb = str(tmpdir.join('notebook.ipynb'))
    tmp_py = str(tmpdir.join('notebook.py'))

    cm = jupytext.TextFileContentsManager()
    cm.root_dir = str(tmpdir)
    cm.default_cell_markers = "'''"

    nb = new_notebook(cells=[new_code_cell('1 + 1'), new_markdown_cell('a\nlong\ncell')],
                      metadata={'jupytext': {'formats': 'ipynb,py',
                                             'notebook_metadata_filter': '-all'}})
    cm.save(model=dict(type='notebook', content=nb), path='notebook.ipynb')

    assert os.path.isfile(tmp_ipynb)
    assert os.path.isfile(tmp_py)

    with open(tmp_py) as fp:
        text = fp.read()

    compare(text, """1 + 1

# a
# long
# cell
""")

    nb2 = jupytext.read(tmp_py)
    compare_notebooks(nb, nb2)


def test_single_triple_quote_works(no_jupytext_version_number, text='''# ---
# jupyter:
#   jupytext:
#     cell_markers: '"""'
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %%
print("hello")
''', notebook=new_notebook(cells=[new_code_cell('print("hello")')])):
    compare_notebooks(jupytext.reads(text, 'py'), notebook)
