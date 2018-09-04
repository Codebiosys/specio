from titlecase import titlecase


def get_jsonable_key(string):
    """ Convert the given string into a usable title for a JSON Key. """
    return titlecase(string.lower().strip())


def get_element_title(element, suffix=None):
    """ Return a human-friendly name for the element with the given suffix.

    Example
    ::

        get_element_title(Element(<a href="#">Profile</a>), suffix='Link')
        >>> 'Profile Link'
    """
    possible_attrs = (
        'title',
        'aria-label',
    )

    possible_title = element.text_content().strip()
    if possible_title:
        return f'{possible_title} {suffix}'

    # The element has no text, so let's try other approaches.
    for attr in possible_attrs:
        possible_title = element.get(attr, '').strip()
        if possible_title:
            return f'{possible_title} {suffix}'


    # Nothing was found.
    return 'UNKNOWN'
