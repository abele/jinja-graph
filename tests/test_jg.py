from jg.__main__ import main, generate_template_graph


def test_main_returns_0_on_successful_execution():
    assert main([]) == 0


def test_returns_graphviz_graph_for_fixture_directory():
    dot = generate_template_graph(root_path='./tests/fixtures')

    assert dot.source == ('digraph {\n\t"index.html"\n'
                          '\t\t"index.html" -> "header.html"\n'
                          '\t\t"index.html" -> "footer.html"\n'
                          '\t"analytics.html"\n'
                          '\t"custom_index.html"\n'
                          '\t\t"custom_index.html" -> "index.html"\n'
                          '\t\t"custom_index.html" -> "snippets/ga.html"\n'
                          '\t"footer.html"\n'
                          '\t"header.html"\n}')
