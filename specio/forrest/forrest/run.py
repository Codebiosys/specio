import logging
import logging.config
import time
import yaml

from watchdog.observers.polling import PollingObserver

from .configuration import Configuration
from .handlers import SpecioEventHandler
from .tasks import pipeline


logger = logging.getLogger(__name__)


def setup_logging(config):
    with open(config.logging_config) as f:
        logging_config = yaml.load(f)

    logging.config.dictConfig(logging_config)


def get_event_handler(config):
    return SpecioEventHandler(
        config.as_dict(),
        patterns=config.patterns,
        ignore_patterns=config.ignore_patterns,
        ignore_directories=config.ignore_directories,
        case_sensitive=config.case_sensitive,
    )


def get_observer(config, handler):
    observer = PollingObserver()
    observer.schedule(
        handler,
        config.path,
        recursive=True
    )
    return observer


def main(run_once=False):
    """ A method that watches files for changes and runs the full pipline. """
    config = Configuration()
    setup_logging(config)

    logger.info('Welcome to Specio!')

    if run_once:
        logger.info(
            'In this mode, Specio will not watch for file changes and must instead '
            'be invoked each time you want to re-run the pipline.'
        )
        configdict = config.as_dict()

        logger.info(f'Dispatching pipeline for {config.input}')
        result = pipeline(configdict, config.input)
        print(result)

        logger.debug(f'Waiting for pipeline to complete...')
        result.get()

        logger.info('Pipeline complete! Exiting.')
        return


    # In the normal run-forever mode.

    event_handler = get_event_handler(config)
    observer = get_observer(config, event_handler)

    logger.info(
        'In this mode, Specio will watch {config.path} for changes invoke the '
        'pipeline each time a ".yml" file changes.'
    )

    observer.start()

    logger.info('Entering runloop. Watching for changes...')

    try:
        while True: time.sleep(1)  # noqa
    except KeyboardInterrupt:
        logger.info('Runloop cancelled by user. Exiting.')
        observer.stop()

    observer.join()
