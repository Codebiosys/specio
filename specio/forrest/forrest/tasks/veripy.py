import logging
import json
from subprocess import Popen, PIPE

from veripy2specio.transforms import Veripy2SpecioTransform

from ..celery import app


logger = logging.getLogger(__name__)


class VeriPyRunError(Exception):
    """ An error was encountered while attempting to run VeriPy. """
    pass


class SpecioConversionError(Exception):
    """ An error was encountered while attempting to convert the VeriPy output
    to the specio format.
    """
    pass


# Command Constants


specio_json = 'specio.json'
cucumber_json = 'cucumber.json'


# Shell Command Templates


veripy_command_template = """\
RESOURCES_DIR={cwd}/resources \
REPORTS_DIR={cwd}/reports \
FIXTURES_DIR={cwd}/fixtures \
behave \
    --outfile {cwd}/reports/{cucumber_json} \
    --format veripy.formatters.cucumber_json:PrettyCucumberJSONFormatter \
    {cwd};
"""


specio_conversion_command = f"""\
veripy2specio -o {specio_json} {cucumber_json};
"""


# Tasks


@app.task
def veripy(run_config, specio_config):
    """ Given a run config, run VeriPy on the features given and return the
    parsed results of the cucumber.json emitted by VeriPy.
    """
    logging.info('Attempting to run VeriPy against run_config.')
    cwd = run_config['input']

    command = veripy_command_template.format(
        cucumber_json=cucumber_json,
        cwd=cwd,
    )
    kwargs = dict(
        universal_newlines=True,
        stderr=PIPE,
        stdout=PIPE,
        shell=True,
        cwd=cwd,
    )

    # Run VeriPy with the given features.
    #
    # NOTE: We chose to use Popen rather than a simpler API because the
    # connection allows us to progressively iterate over stdout/stderr while
    # the program is running.
    logger.debug(f'Running VeriPy in {cwd}')
    with Popen(command, **kwargs) as connection:
        for line in connection.stdout:
            logger.info(line)

        for line in connection.stderr:
            logger.info(line)

        connection.wait()

    # Parse the output and exit.
    with open(f'{cwd}/reports/{cucumber_json}') as f:
        return run_config, json.load(f)


@app.task
def convert_to_specio(previous_results, specio_config):
    """ Given a run config and set of results from VeriPy, convert the results
    to the Specio format.
    """
    logging.info('Attempting to convert VeriPy output to Specio format.')
    # Unpack the previous results.
    run_config, veripy_results = previous_results

    transform = Veripy2SpecioTransform()
    specio_json = transform(veripy_results)

    return run_config, specio_json
