# Components


feature = {
    'type': 'object',
    'properties': {
        'test_purpose_format': {'type': 'string'},
    },
    'required': [
        'name',
    ],
}


organization = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'feature' : feature,
    },
    'required': [
        'name',
    ],
}


environment = {
    'type': 'object',
    'properties': {
        'browser_name': {'type': 'string'},
        'browser_version': {'type': 'string'},
        'os_name': {'type': 'string'},
        'os_version': {'type': 'string'},
        'specio_version': {'type': 'string'},
    },
    'required': [
        'browser_name',
        'browser_version',
        'os_name',
        'os_version',
        'specio_version',
    ],
}


# Overall Schema


schema = {
    'type': 'object',
    'properties': {
        'environment': environment,
        'organization': organization,
        'run_date': {'type': 'number'},
        'specio_operator': {'type': 'string'},
    },
    'required': [
        'environment',
        'organization',
        'run_date',
        'specio_operator',
    ],
}
