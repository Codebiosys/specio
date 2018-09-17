import json
import time

from watchdog.observers.polling import PollingObserver

from .configuration import Configuration
from .handlers import SpecioEventHandler


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

    event_handler = get_event_handler(config)
    observer = get_observer(config, event_handler)

    observer.start()

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
