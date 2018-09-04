import lxml.html
from lxml import etree

from . import formatters


""" The list of extractors to run.
All extractors must take 2 parameters: the HTML input and the app config.
Each extractor should return a list of found items that match its criteria in
the following format:
::

    [
        "key": {
            "selector": "<selector>",
            "by": "<selector type>",
        }
        # ...
    ]

"""
extractors = (
    ('//a', formatters.format_link),
    ('//button', formatters.format_button),
    ('//title', formatters.format_page_title),
)


# Public Extraction Functions


def extract(html, config):
    tree = etree.ElementTree(lxml.html.fromstring(html))
    return {
        'url': '',
        'elements': {
            item_name: formatted_item
            for path, formatter in extractors
            for item_name, formatted_item in formatter(
                tree.findall(path),
                config,
                path,
                tree
            )
        },
    }
