import logging

from watchdog.events import PatternMatchingEventHandler

from .tasks import pipeline


logger = logging.getLogger(__name__)


class SpecioEventHandler(PatternMatchingEventHandler):

    def __init__(self, configdict, **kwargs):
        self.configdict = configdict
        super().__init__(**kwargs)

    def on_created(self, event):
        if event.is_directory:
            # Ignore directory changes.
            return
        self._kickoff(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            # Ignore directory changes.
            return
        self._kickoff(event.src_path)

    def _kickoff(self, path):
        if path.endswith('.lock'):
            logger.debug('Found lockfile. Ignoring...')
        elif path.endswith('.yml'):
            logger.info(f'Dispatching pipeline for {path}')
            pipeline(self.configdict, path)
        else:
            logger.info('Non-config File detected. Ignoring...')
