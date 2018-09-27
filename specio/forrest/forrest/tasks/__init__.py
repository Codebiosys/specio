import logging

from celery import chain

from ..celery import app
from . import fs, pdfs, veripy


logger = logging.getLogger(__name__)


@app.task
def debug_task():
    logger.debug('Hello')


@app.task
def log_error(specio_config, inputfilepath, request, exc, traceback):
    logger.error(traceback)


@app.task
def completion(inputfilepath):
    logger.info(f'Workflow complete for file: {inputfilepath}')
    # TODO: Send email to someplace about completion.


@app.task
def pipeline(specio_config, inputfilepath):
    """ The Main Workflow for the Specio Pipeline.

    This task dispatches a celery workflow to process the given input config file
    using the given specio configuration. This workflow is broken up into several
    parts, each of which can be run on a separate machine or VM.

    Logs and Errors from each task are logged to the central logging system.

    Usage
    -----

        from run.forrest import tasks
        tasks.pipeline.delay()


    Implementation Notes
    --------------------

    Each of the tasks contained within this workflow are entirely idempotent and
    functional. Some of the tasks do require a file system state, but any required
    state should be provided by the docker volume.

    Any tasks that write to the filesystem automatically clean up after themselves
    leaving the disk in a non-polluted state.

    """
    logger.debug(f'Constructing Specio workflow for: {inputfilepath}')
    workflow = chain(
        # Attempt to acquire a lock for the given run
        fs.acquire_lock.si(specio_config, inputfilepath).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Load in the specio_config
        fs.get_run_config.si(specio_config, inputfilepath).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Do specio_config validation
        fs.validate_run_config.s(specio_config).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Run VeriPy
        veripy.veripy.s(specio_config).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Convert the output of VeriPy to the Specio format
        veripy.convert_to_specio.s(specio_config).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Get the PDF report
        pdfs.get_report.s(specio_config).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Write the report to disk
        fs.write_report.s(specio_config).on_error(
            log_error.s(specio_config, inputfilepath)
        ),

        # Release the lock
        fs.release_lock.si(specio_config, inputfilepath).on_error(
            log_error.s(specio_config, inputfilepath)
        ),
        # Log the completion.
        completion.si(inputfilepath).on_error(
            log_error.s(specio_config, inputfilepath)
        ),
    )
    return workflow()
