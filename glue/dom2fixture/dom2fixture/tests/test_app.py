import json
import os.path

import pytest


FIXTURE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))


@pytest.fixture(params=[
    {
        'url': 'https://google.com/test',
        'verbose': True,
        'input': 'google-search-results.html',
        'output': 'google-search-results.json',
    },
    {
        'url': 'https://pine.blog',
        'verbose': True,
        'input': 'pine.blog.html',
        'output': 'pine.blog.json',
    },
])
def valid_configuration(request):
    class MockConfig(object):
        file_entries = (('input', 'r'), ('output', 'r'))

        def __init__(self):
            entries = {**request.param}

            for filename, mode in self.file_entries:
                entries[filename] = open(
                    os.path.join(FIXTURE_PATH, entries[filename]),
                    mode
                )

            self.__dict__.update(**entries)

        def cleanup(self):
            for filename, _ in self.file_entries:
                getattr(self, filename).close()

    config = MockConfig()
    try:
        yield config
    finally:
        config.cleanup()


def test_load_input__valid_schema(valid_configuration):
    from dom2fixture import app
    input = valid_configuration.input.read()
    output = app.extract(input, valid_configuration)
    fixture = json.load(valid_configuration.output)
    assert output == fixture
