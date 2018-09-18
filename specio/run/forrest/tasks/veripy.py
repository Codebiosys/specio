import logging
import json
import os
import shlex
from shutil import copytree
from subprocess import run, Popen, STDOUT, PIPE, CalledProcessError
import tempfile
from uuid import uuid4

from veripy2specio.transforms import Veripy2SpecioTransform

from run.forrest.celery import app


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
TMP_DIRECTORY={cwd}/tmp \
behave \
    -o {cwd}/reports/{cucumber_json} \
    -f formatters.cucumber_json:PrettyCucumberJSONFormatter \
    {veripy_features};
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
    with tempfile.TemporaryDirectory() as cwd:
        logger.debug(f'VeriPy working directory: {cwd}')
        features_dir = f'{cwd}/features'

        # Copy the features in from the configured location into the tmp directory.
        logger.debug(f'Copying features to {cwd}')
        copytree(run_config['features'], features_dir)

        # Symlink the features from the current directory into VeriPy so that
        # they can be run.
        logger.debug(f'Symlinking {features_dir} to {specio_config["veripy_features"]}')
        os.symlink(
            features_dir,
            specio_config['veripy_features'],
            target_is_directory=True
        )

        # Command setup

        command = veripy_command_template.format(
            veripy_features=specio_config['veripy_features'],
            cucumber_json=cucumber_json,
            cwd=cwd,
        )
        kwargs = dict(
            universal_newlines=True,
            stderr=PIPE,
            stdout=PIPE,
            shell=True,
            cwd='/app',
        )

        # Run VeriPy with the given features.
        #
        # NOTE: We chose to use Popen rather than a simpler API because the
        # connection allows us to progressively iterate over stdout/stderr while
        # the program is running.
        logger.debug(f'Running VeriPy in {cwd}')
        with Popen(command, **kwargs) as connection:
            for line in connection.stdout:
                # TODO: Replace with logging.
                print(line)

            for line in connection.stderr:
                # TODO: Replace with logging.
                print(line)

            connection.wait()

        # Clean up the symlinks so they don't pollute the fs.
        logger.debug(f'Cleaning up symlinks.')
        os.unlink(specio_config['veripy_features'])

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
