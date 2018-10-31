from base64 import b64decode
from datetime import datetime
import logging
import os
import os.path
import shutil
import yaml

from ..celery import app


logger = logging.getLogger(__name__)


class FailedToAcquireLock(Exception):
    """ During processing, a lock could not be acquired on a given project,
    probably because the project already has a lock on it.
    """
    pass


class FailedToReleaseLock(Exception):
    """ During processing, a lock could not be released from a given project,
    probably because the lock was released by another instance running the project.

    IMPORTANT:
    ----------

    This is a fairly serious error since it means that two or more instances of
    the app were running at once. This is not expected!
    """
    pass


# Locking Tasks


@app.task
def acquire_lock(kwargs):
    """ Attempt to acquire the lock on the input file. """
    inputfilepath, specio_config = kwargs['inputfilepath'], kwargs['specio_config']

    logger.info(f'Attempting to acquire lock for file: {inputfilepath}')
    lockfile = f'{inputfilepath}.lock'

    # Ensure that we haven't attempted to run an already running file.
    # The user can also force the run to occur and in that case we ignore the
    # lockfile and overwrite it.
    # TODO: We might want to parse the date of the run and ensure that it's
    # not referring to a run that might have expired...
    if specio_config['force']:
        logger.info('Run was forced! Ignoring lockfile.')
        logger.warning(
            'Be careful when forcing runs. Lockfiles ensure that the same test '
            'isn\'t being run more than once at a time. Multiple concurrent, identical '
            'runs is not supported and can cause unexpected results.'
        )
    elif os.path.exists(lockfile):
        raise FailedToAcquireLock(f'Lockfile for {inputfilepath} already exists.')

    now = datetime.now().isoformat()
    lockfile_contents = (
        f'Lock acquired on {now}'
    )

    with open(lockfile, 'w') as f:
        f.write(lockfile_contents)

    logger.debug(f'Lock obtained for file: {inputfilepath}')
    return kwargs


@app.task
def release_lock(kwargs):
    """ Attempt to release the lock on the original input file. """
    inputfilepath = kwargs['inputfilepath']

    logger.info(f'Attempting to release lock for file: {inputfilepath}')
    lockfile = f'{inputfilepath}.lock'

    # Ensure that we haven't attempted to release a non-running file.
    if not os.path.exists(lockfile):
        raise FailedToReleaseLock(
            f'Unable to release lock. Was another run working at the same time?\n'
            f'Lockfile for {inputfilepath} doesn\'t exist.'
        )

    os.remove(lockfile)
    logger.debug(f'Lock released for file: {inputfilepath}')
    return kwargs


# I/O Tasks


@app.task
def get_run_config(kwargs):
    """ Given an input file path, return a dict of the config options for the
    current run.

    :returns: run_config
    """
    inputfilepath = kwargs['inputfilepath']

    logger.info(f'Attempting to parse run config for {inputfilepath}')
    with open(inputfilepath) as f:
        return {
            **kwargs,
            'run_config': yaml.load(f),
        }


@app.task
def write_report(kwargs):
    """ Given a reportblob, write the report to the desired output location. """
    run_config, report_blob = kwargs['run_config'], kwargs['report_blob']

    logger.info(f'Attempting to write report.')
    with open(run_config['output'], 'wb') as f:
        f.write(b64decode(report_blob.encode('ascii')))
    return kwargs


@app.task
def copy_recording(kwargs):
    if kwargs['specio_config']['no_video']:
        # No video was created. Skip.
        return kwargs

    location, run_config = kwargs['video_location'], kwargs['run_config']

    logger.info(f'Attempting to copy test recording.')
    shutil.copy(location, run_config['recording_output'])
    return kwargs


@app.task
def copy_subtitles(kwargs):
    if kwargs['specio_config']['no_video']:
        # No video was created. Skip.
        return kwargs

    location, run_config = kwargs['subtitles_file'], kwargs['run_config']
    recording_location = run_config["recording_output"]

    logger.info(f'Attempting to copy test subtitles.')
    shutil.copy(location, f'{recording_location}.srt')
    return kwargs


# Validation Tasks


@app.task
def validate_run_config(kwargs):
    """ Given a run config, validate it and if it is valid, return it.

    :returns: run_config
    """
    logger.info(f'Attempting to validate run config.')

    # TODO: Validate Run Config, for now write a warning.
    logger.warning('No validation is currently being done. Please review and add.')

    return kwargs
