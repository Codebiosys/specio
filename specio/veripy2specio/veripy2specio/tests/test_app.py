import json
import os.path

import pytest

FIXTURE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))


@pytest.fixture(params=[
    {
        'verbose': True,
        'input': 'valid_schema.json',
        'output': 'output.json',
    },
    {
        'verbose': False,
        'input': 'valid_schema.json',
        'output': 'output.json',
    },
])
def valid_configuration(request):
    class MockConfig(object):
        file_entries = (('input', 'r'), ('output', 'w'))

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
    yield config
    config.cleanup()


def test_load_input__valid_schema(valid_configuration):
    from veripy2specio import app
    assert app.load_input(valid_configuration) is not None
