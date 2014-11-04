import re
import sys
from itertools import chain

import py
from graphviz import Digraph


EXTENDS_RE = re.compile(r'{%\s*extends\s*[\'"](.*)[\'"]\s*%}')
INCLUDE_RE = re.compile(r'{%\s*include\s*[\'"](.*)[\'"]\s*%}')
TEMPLATE_PATTERN = '*.html'


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
    node_name_and_template_path = ((_node_name(path, cwd), path)
                                   for path in _template_path_seq(root_path))
    dot = Digraph()

    for node_name, template_path in node_name_and_template_path:
        dot.node(node_name)
        file_content = template_path.read()
        derived_file_seq = chain(
            EXTENDS_RE.findall(file_content),
            INCLUDE_RE.findall(file_content)
        )
        for derived_file_path in derived_file_seq:
            dot.edge(node_name, derived_file_path)

    return dot


def _node_name(path, cwd):
    return path.strpath.replace(cwd.strpath, '', 1).lstrip('/')


def _template_path_seq(root_path):
    return py.path.local(root_path).visit(TEMPLATE_PATTERN)


if __name__ == "__main__":
    sys.exit(main())
