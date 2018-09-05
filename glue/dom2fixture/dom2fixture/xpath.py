def get_shortest_xpath(tree, element, path=None):
    """ A method that attempts to return the shortest possible unique xpath for
    a given element.

    To do this, we simply lop off the front of the XPath until the path doesn't
    uniquely describe the given element.
    """

    if path is None:
        path = tree.getpath(element)

    lop_index = 3 if path.startswith('//') else 2
    new_path = '//' + '/'.join(path.split('/')[lop_index:])

    if tree.find(new_path) == element and len(tree.findall(new_path)) == 1:
        return get_shortest_xpath(tree, element, path=new_path)

    return path
