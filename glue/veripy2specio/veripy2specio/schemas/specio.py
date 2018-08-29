# Components


organization = {
    'type' : 'object',
    'properties' : {
        'name': {'type': 'string'},
    },
}


step_attachment = {
    'type' : 'object',
    'required': ['name', 'data'],
    'properties' : {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'data': {'type': 'string'},
    },
}


step = {
    'type' : 'object',
    'required': ['name'],
    'properties' : {
        'name': {'type': 'string'},
        'value': {'type': 'string'},
        'attachments': {
            'type': 'array',
            'items': step_attachment,
        },
    },
}


scenario = {
    'type' : 'object',
    'required': ['steps', 'name'],
    'properties' : {
        'name': {'type': 'string'},
        'steps': {
            'type' : 'array',
            'items': step,
        },
    },
}


feature = {
    'type' : 'object',
    'required': ['scenarios', 'name'],
    'properties' : {
        'name': {'type': 'string'},
        'scenarios': {
            'type' : 'array',
            'items': scenario,
        },
    },
}


# Overall Schema


schema = {
    'type': 'object',
    'required': ['features', 'organization'],
    'properties' : {
        'organization' : organization,
        'features' : {
            'type' : 'array',
            'items': feature,
        },
    },
}

