import logging, logging.config
import time
import yaml

from watchdog.observers.polling import PollingObserver

from .configuration import Configuration
from .handlers import SpecioEventHandler


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


def main():
    config = Configuration()

    setup_logging(config)
    event_handler = get_event_handler(config)
    observer = get_observer(config, event_handler)

    observer.start()

    logger.info('Entering runloop. Watching for changes...')

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        logger.info('Runloop cancelled by user. Exiting.')
        observer.stop()

    observer.join()
