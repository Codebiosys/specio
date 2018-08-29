import json

from veripy2specio.configuration import Configuration
from veripy2specio.schemas import validate, INPUT_SCHEMA, OUTPUT_SCHEMA
from veripy2specio.transforms import Veripy2SpecioTransform


def load_input(config):
    input = json.load(config.input)
    validate(input, INPUT_SCHEMA)
    return input


def dump_output(output, config):
    validate(output, OUTPUT_SCHEMA)
    config.output.write(json.dumps(output))


def main():
    config = Configuration()

    if config.verify_veripy:
        # Don't do any transformation, just validate.
        input = json.load(config.input)
        validate(input, INPUT_SCHEMA)
    elif config.verify_specio:
        # Don't do any transformation, just validate.
        input = json.load(config.input)
        validate(input, OUTPUT_SCHEMA)
    else:
        # Convert the file.
        input = load_input(config)
        transform = Veripy2SpecioTransform(config)
        output = transform(input)
        dump_output(output, config)
