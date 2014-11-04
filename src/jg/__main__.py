import re
import sys

import py
from graphviz import Digraph
from itertools import chain


EXTENDS_RE = re.compile(r'{%\s*extends\s*[\'"](.*)[\'"]\s*%}')
INCLUDE_RE = re.compile(r'{%\s*include\s*[\'"](.*)[\'"]\s*%}')

def main(argv=()):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    print(argv)
    return 0


def generate_template_graph(root_path):
    cwd = py.path.local(root_path)
    assert cwd == '/home/abele/Devel/jinja-graph/tests/fixtures'
    template_path_list = py.path.local(root_path).listdir(
        fil=lambda p: p.isfile()
    )
    template_dict = {path.strpath.replace(cwd.strpath, '', 1).lstrip('/'): {'path': path} for path in template_path_list}
    dot = Digraph()

    for rel_path in template_dict:
        dot.node(rel_path)

        file_content = template_dict[rel_path]['path'].read()
        derived_file_seq = chain(
            EXTENDS_RE.findall(file_content),
            INCLUDE_RE.findall(file_content)
        )
        for derived_file_path in derived_file_seq:
            dot.edge(rel_path, derived_file_path)

    return dot


if __name__ == "__main__":
    sys.exit(main())
