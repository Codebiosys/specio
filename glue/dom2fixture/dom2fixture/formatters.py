import uuid

from .xpath import get_shortest_xpath
from .utils import get_element_title


def format_element(element, config, extractor, tree):
    """ A general element formatter. Useful for testing, but not much else. """
    for e in element:
        title = get_element_title(e, suffix='Element')
        yield title, {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }


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


def format_input(element, config, extractor, tree):
    """ Formats elements that are inputs. """
    for id, e in enumerate(element):
        # Try getting the normal names.
        possible_title = get_element_title(e, suffix='Field', no_default=True)

        if not possible_title:
            # Try using the nearest parent.
            possible_title = get_element_title(
                e.getparent(),
                suffix='Field',
                no_default=True
            )

        if not possible_title:
            # Try using the input's given label using for="".
            associated_labels = (
                tree.find(f'//label[@for="{name}"]')
                for name in (
                    e.get('name'),
                    e.get('id'),
                    *e.get('class', '').split(),
                )
                if name
            )
            for associated_label in associated_labels:
                if associated_label is not None:
                    possible_title = get_element_title(
                        associated_label,
                        suffix='Field',
                        no_default=True
                    )
                    break

        if not possible_title:
            possible_title = f'Unknown Field {id}'

        yield possible_title, {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }


def format_header(element, config, extractor, tree):
    """ Formats elements that are headers. """
    for e in element:
        title = get_element_title(e, suffix='Header')
        yield title, {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }


def format_image(element, config, extractor, tree):
    """ Formats elements that are images. """
    for e in element:
        title = get_element_title(e, suffix='Image')
        yield title, {
            'selector': get_shortest_xpath(tree, e),
            'by': 'xpath',
        }

