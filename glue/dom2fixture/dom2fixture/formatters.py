from .xpath import get_shortest_xpath
from .utils import get_element_title


def format_element(element, config, extractor, tree):
    """ A general element formatter. Useful for testing, but not much else. """
    for e in element:
        name = extractor

        formatted_e =  {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }

        yield name, formatted_e


def format_page_title(element, config, extractor, tree):
    """ Formats elements that are page titles. """
    for e in element:
        yield 'Page Title', {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }


def format_link(element, config, extractor, tree):
    """ Formats elements that are links. """
    for e in element:
        title = get_element_title(e, suffix='Link')
        yield title, {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }


def format_button(element, config, extractor, tree):
    """ Formats elements that are buttons. """
    for e in element:
        title = get_element_title(e, suffix='Button')
        yield title, {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }


