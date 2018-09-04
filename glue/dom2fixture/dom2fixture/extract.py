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
    # Page Elements

    ('//title', formatters.format_page_title),

    # Interactive Elements

    ('//a', formatters.format_link),
    ('//button', formatters.format_button),
    ('//input', formatters.format_input),

    # Headers

    ('//h1', formatters.format_header),
    ('//h2', formatters.format_header),
    ('//h3', formatters.format_header),
    ('//h4', formatters.format_header),
    ('//h5', formatters.format_header),
    ('//h6', formatters.format_header),

    # Media

    ('//img', formatters.format_image),
)


# Public Extraction Functions


def extract(html, config):
    tree = etree.ElementTree(lxml.html.fromstring(html))
    return {
        'url': config.url,
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
