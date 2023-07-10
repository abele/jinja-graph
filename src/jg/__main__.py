import re
import sys
from itertools import chain
import argparse

import py
from graphviz import Digraph


EXTENDS_RE = re.compile(r'{%\s*extends\s*[\'"](.*)[\'"]\s*%}')
INCLUDE_RE = re.compile(r'{%\s*include\s*[\'"](.*)[\'"]\s*%}')
IMPORT_RE = re.compile(r'{%-?\s*import\s*[\'"](.*)[\'"]\s*')
SECOND_IMPORT_RE = re.compile(r'{%-?\s*from\s*[\'"](.*)[\'"]\s*import\s*')


def main(argv=()):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """
    parser = argparse.ArgumentParser(
        description="Generate Jinja template dependency graph"
    )
    parser.add_argument("-i", "--input", default="./", help="Root path", required=True)
    parser.add_argument(
        "-o", "--output", default="./output.dot", help="Output filename", required=True
    )
    parser.add_argument(
        "-e",
        "--extension",
        default=".html",
        help="The extension to search for dependency tree, examples: .html, .j2, .css, .txt",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="Reverse the graph"
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Print the TOP 10 referenced items"
    )

    args = parser.parse_args(argv or sys.argv[1:])
    root_path = args.input
    output_filename = args.output
    TEMPLATE_PATTERN = f"*{args.extension}"

    dot = generate_template_graph(
        root_path=root_path, template_pattern=TEMPLATE_PATTERN, reverse=args.reverse, print_top_10=args.print
    )

    write(dot.source, output_filename)

    return 0


def write(content, output_filename):
    py.path.local(output_filename).write(content, ensure=True)


def generate_template_graph(root_path, template_pattern: str, reverse: bool = False, print_top_10: bool = False):
    cwd = py.path.local(root_path)
    node_name_and_template_path = (
        (_node_name(path, cwd), path)
        for path in _template_path_seq(root_path, template_pattern=template_pattern)
    )
    dictionary = {}

    for node_name, template_path in node_name_and_template_path:
        if not reverse and dictionary.get(node_name) is None:
            dictionary[node_name] = []
        file_content = template_path.read()

        derived_file_seq = chain(
            EXTENDS_RE.findall(file_content),
            INCLUDE_RE.findall(file_content),
            IMPORT_RE.findall(file_content),
            SECOND_IMPORT_RE.findall(file_content),
        )
        for derived_file_path in derived_file_seq:
            if reverse:
                if dictionary.get(derived_file_path) is None:
                    dictionary[derived_file_path] = []

                dictionary[derived_file_path].append({"source": derived_file_path, "target": node_name})
            else:
                dictionary[node_name].append({"source": node_name, "target": derived_file_path})

    dot = Digraph()

    for key in dictionary.keys():
        dot.node(key)
        for item in dictionary.get(key):
            dot.edge(item.get('source'), item.get('target'))

    if print_top_10:
        print(' '.join(sorted(dictionary, key=lambda k: len(dictionary[k]), reverse=True)[:10]))

    return dot


def _node_name(path, cwd):
    return path.strpath.replace(cwd.strpath, "", 1).lstrip("/")


def _template_path_seq(root_path, template_pattern: str):
    return py.path.local(root_path).visit(template_pattern)


if __name__ == "__main__":
    sys.exit(main())
