import json

from dom2fixture.configuration import Configuration
from dom2fixture.extract import extract


def main():
    config = Configuration()

    input = config.input.read()
    output = extract(input, config)
    config.output.write(json.dumps(output, indent='\t'))
