from jg.__main__ import main, generate_template_graph
from mock import patch


FIXTURE_GRAPH = (
        'digraph {\n'
        '\t"snippets/sub/analytics.html"\n'
        '\t"snippets/ga.html"\n'
        '\t\t"snippets/ga.html" -> "snippets/sub/analytics.html"\n'
        '\t"header.html"\n'
        '\t"analytics.html"\n'
        '\t"custom_index.html"\n'
        '\t\t"custom_index.html" -> "index.html"\n'
        '\t\t"custom_index.html" -> "snippets/ga.html"\n'
        '\t"index.html"\n'
        '\t\t"index.html" -> "header.html"\n'
        '\t\t"index.html" -> "footer.html"\n'
        '\t"footer.html"\n}')


def test_main_generates_graph_for_given_directory():
    output_filename = 'graph.dot'
    with patch('jg.__main__.write') as write:
        exit_code = main(['./tests/fixtures', output_filename])

    write.assert_called_with(FIXTURE_GRAPH, output_filename)
    assert exit_code == 0


def test_parses_all_templates_in_given_root_directory():
    dot = generate_template_graph(root_path='./tests/fixtures')
    dot.render('t1.dot')
    assert dot.source == FIXTURE_GRAPH
