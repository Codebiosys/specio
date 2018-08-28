# Components

tag = {}


step = {
    'type': 'object',
    'properties': {
        'keyword': {'type': 'string'},
        'line': {'type': 'integer'},
        'name': {'type': 'string'},
        'match': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string'
                }
            },
            'required': [
                'location'
            ]
        },
        'result': {
            'type': 'object',
            'properties': {
                'duration': {'type': 'integer'},
                'status': {'type': 'string'}
            },
            'required': [
                'duration',
                'status'
            ]
        },
        'step_type': {'type': 'string'}
    },
    'required': [
        'keyword',
        'line',
        'match',
        'name',
        'result',
        'step_type'
    ]
}


scenario = {
    'type': 'object',
    'properties': {
        'description': {'type': 'string'},
        'id': {'type': 'string'},
        'keyword': {'type': 'string'},
        'line': {'type': 'integer'},
        'location': {'type': 'string'},
        'name': {'type': 'string'},
        'type': {'type': 'string'},
        'steps': {
            'type': 'array',
            'items': step,
        },
        'tags': {
            'type': 'array',
            'items': tag
        },
  },
  'required': [
    'description',
    'id',
    'keyword',
    'line',
    'location',
    'name',
    'steps',
    'tags',
    'type'
  ]
}


# Overall Schema


schema = {
    'type': 'array',
    'items': [
        {
          'type': 'object',
          'properties': {
            'description': {'type': 'string'},
            'elements': {
              'type': 'array',
              'items': scenario
            },
            'id': {'type': 'string'},
            'keyword': {'type': 'string'},
            'line': {'type': 'integer'},
            'name': {'type': 'string'},
            'status': {'type': 'string'},
            'uri': {'type': 'string'},
            'tags': {
                'type': 'array',
                'items': tag
            },
          },
          'required': [
            'description',
            'elements',
            'id',
            'keyword',
            'line',
            'name',
            'status',
            'tags',
            'uri'
          ]
        }
    ]
}
