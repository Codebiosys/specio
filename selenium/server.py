import logging
import os
import os.path
import shlex
from subprocess import Popen, CalledProcessError
from uuid import uuid4

from flask import Flask, jsonify, request


app = Flask(__name__)

logging.basicConfig()
logger = logging.getLogger(__name__)


DISPLAY = os.getenv('DISPLAY', ':99.0')
DEFAULT_SIZE = '{width}x{height}'.format(
    width=os.getenv('SCREEN_WIDTH', '640'),
    height=os.getenv('SCREEN_HEIGHT', '480'),
)
PREFERRED_VIDEO_FORMAT = os.getenv('PREFERRED_VIDEO_FORMAT', 'mpg')
OUTPUT_VOLUME = os.getenv('OUTPUT_VOLUME', '/opt/recordings')


FFMPEG_CMD = """\
sudo ffmpeg -f x11grab -video_size {size} {input_options} -i {display} {output_options} {output}"""

START_RECORDING_CMD = """\
tmux new-session -d -s {session_id} '{ffmpeg_cmd}'"""

STOP_RECORDING_CMD = """\
tmux send-keys -t {session_id} q"""


@app.route('/', methods=('GET',))
def hello():
    return 'Welcome Acknowledged'


@app.route('/start', methods=('POST',))
def start_recording():
    """ This endpoint generates a session identifier for the given selenium
    test run, and starts the recording session in a background context.

    To interact with the recording later (i.e. to stop it) supply the stop
    endpoint with the session identifier.
    """
    logger.info('Starting recording.')
    session_id = uuid4().hex
    output = '{path}.{format}'.format(
        path=os.path.join(OUTPUT_VOLUME, session_id),
        format=PREFERRED_VIDEO_FORMAT,
    )

    ffmpeg_command = FFMPEG_CMD.format(
        size=request.form.get('size', DEFAULT_SIZE),
        input_options=request.form.get('input_options', ''),
        display=DISPLAY,
        output_options=request.form.get('output_options', ''),
        output=output,
    )
    start_command = START_RECORDING_CMD.format(
        session_id=session_id,
        ffmpeg_cmd=ffmpeg_command,
    )

    logger.info('Running command:', start_command)

    try:
        process = Popen(shlex.split(start_command))
        logger.info(process.stdout, process.stderr)
    except CalledProcessError as e:
        logging.critical(e.args)
        error = ' '.join(e.args)
        status = 400
    else:
        error = None
        status = 200

    return jsonify(
        session_id=session_id,
        output=output,
        error=error
    ), status


@app.route('/stop', methods=('POST',))
def stop_recording():
    """ Given a recording session id, cancel the FFmpeg x11 capture or return any
    errors that might occur.

    Note: Errors with cancelling the stream will result in a 400 and an error
    parameter, while errors in other aspects will return a 500.
    """
    logger.info('Stopping recording.')
    stop_command = STOP_RECORDING_CMD.format(
        session_id=request.form['session_id'],
    )

    logger.info('Running command:', stop_command)

    try:
        Popen(shlex.split(stop_command))
    except CalledProcessError as e:
        logging.critical(e.args)
        error = ' '.join(str(a) for a in e.args)
        status = 400
    else:
        error = None
        status = 200

    return jsonify(
        error=error,
    ), status


if __name__ == "__main__":
    app.run()
