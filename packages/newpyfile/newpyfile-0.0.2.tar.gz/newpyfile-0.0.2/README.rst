NewPyFile
------------

Create one[or more] python files from your CLI.

Installation
************

>>> pip install newpyfile

Documentation
*************

>>> newpyfile file [file1...]
"""
Creates file.py in the current directory.
"""

>>> newpyfile file --path=path
"""
Creates file.py in the given as path directory.
"""

>>> newpyfile file --imports=a:b:c,d,e
"""
Creates a file in the current directory, importing from package a, subpackages c & d, and
importing packages d & e
"""

>>> newpyfile file --path=path --imports=a:b:c,d,e
"""
Creates a file in the given as path directory, importing from package a, subpackages c & d, and importing packages d & e
"""

>>> newpyfile --file=path
"""
Creates a file/files with names from the given as path file.
"""

Example
*******

>>> newpyfile file1 file2 --imports=datetime:datetime

Your folder now should contain file1.py & file2.py and each file
will have ``from datetime import datetime``

Let's say some_file.txt has the following content:

a b c
d
e

>>> newpyfile --file=some_file

Your folder now should contain a.py, b.py, c.py, d.py and e.py.

LICENSE
*******

``MIT License``


UPDATES
*******

``version 0.0.2``

>>> New option for creating files from a file ``--file=path``.