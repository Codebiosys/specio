import logging
import json
from subprocess import Popen, PIPE
from time import time
from datetime import datetime, timedelta

from veripy2specio.transforms import Veripy2SpecioTransform

from ..celery import app


logger = logging.getLogger(__name__)


class Subtitle(object):

    SRT_TIME = '{hour}:{min}:{sec},{milli}'

    def __init__(self, entry_number, start_time, end_time, text):
        self.entry_number = entry_number
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def format_td(self, td):
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = td.microseconds / 1000

        return f'{int(hours)}:{int(minutes)}:{int(seconds)},{int(milliseconds)}'

    def __str__(self):
        text = self.text.strip()

        return (
            f'{self.entry_number}\n'
            f'{self.format_td(self.start_time)} --> {self.format_td(self.end_time)}\n'
            f'{text}\n\n'
        )


# Command Constants


specio_json = 'specio.json'
cucumber_json = 'cucumber.json'


# Shell Command Templates


veripy_command_template = """\
SETUP_DIR={cwd}/features \
RESOURCES_DIR={cwd}/resources \
REPORTS_DIR={cwd}/reports \
FIXTURES_DIR={cwd}/fixtures \
behave \
    --outfile={cwd}/reports/{cucumber_json} \
    --format veripy.formatters.cucumber_json:PrettyCucumberJSONFormatter \
    --outfile=- \
    --format plain \
    {cwd};
"""


# Tasks


@app.task
def veripy(kwargs):
    """ Given a run config, run VeriPy on the features given and return the
    parsed results of the cucumber.json emitted by VeriPy.
    """
    run_config = kwargs['run_config']

    logging.info('Attempting to run VeriPy against run_config.')
    cwd = run_config['input']

    command = veripy_command_template.format(
        cucumber_json=cucumber_json,
        cwd=cwd,
    )
    cmd_kwargs = dict(
        universal_newlines=True,
        stderr=PIPE,
        stdout=PIPE,
        shell=True,
        cwd=cwd,
    )

    suite_starttime = datetime.fromtimestamp(kwargs['video_starttime'])
    previous_subtitle = None
    record_subtitles = False
    subtitles_filename = kwargs['video_location'] + '.srt'

    # Run VeriPy with the given features.
    #
    # NOTE: We chose to use Popen rather than a simpler API because the
    # connection allows us to progressively iterate over stdout/stderr while
    # the program is running.
    logger.debug(f'Running VeriPy in {cwd}')
    with Popen(command, **cmd_kwargs) as connection, open(subtitles_filename, 'w') as subtitles:
        for line in connection.stdout:
            logger.info(line)

            # Don't record the junk that comes before the features, wait for
            # behave to get started
            record_subtitles = record_subtitles or 'Feature' in line
            if not record_subtitles:
                continue

            now = datetime.fromtimestamp(time()) - suite_starttime

            # Create a new entry for the current line and save it for later.
            entry_number, start = (
                (0, previous_subtitle.end_time)
                if previous_subtitle
                else (0, timedelta(seconds=0))
            )
            previous_subtitle = Subtitle(
                entry_number + 1,
                start,
                now,
                line
            )
            subtitles.write(str(previous_subtitle))

        for line in connection.stderr:
            logger.info(line)

        connection.wait()

    # Parse the output and exit.
    with open(f'{cwd}/reports/{cucumber_json}') as f:
        return {
            **kwargs,
            'veripy_results': json.load(f),
            'subtitles_file': subtitles_filename,
        }


@app.task
def convert_to_specio(kwargs):
    """ Given a run config and set of results from VeriPy, convert the results
    to the Specio format.
    """
    veripy_results = kwargs['veripy_results']

    logging.info('Attempting to convert VeriPy output to Specio format.')
    transform = Veripy2SpecioTransform()
    specio_json = transform(veripy_results)

    return {
        **kwargs,
        'specio_results': specio_json,
    }
