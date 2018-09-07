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
    'properties' : {
        'name': {'type': 'string'},
        'value': {'type': 'string'},
        'passed': {'type': 'boolean'},
        'attachments': {
            'type': 'array',
#             'items': step_attachment,
        },
    },
    'required': [
        'name',
        'passed'
    ],
}


step_group = {
    'type': 'object',
    'properties': {
        'given_when': {
            'type' : 'array',
            'items': step,
        },
        'then': {
            'type' : 'array',
            'items': step,
        },
    },
    'required': [
        'given_when',
        'then',
    ],
}


scenario = {
    'type' : 'object',
    'properties' : {
        'number': {'type': 'number'},
        'name': {'type': 'string'},
        'all_passed': {'type': 'boolean'},
        'steps': {
            'type' : 'array',
            'items': step_group,
        },
    },
    'required': [
        'steps',
        'name',
        'number',
        'tags',
        'all_passed'
    ],
}


feature = {
    'type' : 'object',
    'properties' : {
        'name': {'type': 'string'},
        'scenario_tags': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        'scenarios': {
            'type' : 'array',
            'items': scenario,
        },
    },
    'required': [
        'name',
        'scenarios',
        'scenario_tags',
        'tags'
    ],
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

