from watchdog.events import PatternMatchingEventHandler

from run.forrest.tasks import pipeline


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
            # Silently ignore lockfiles.
            pass
        elif path.endswith('.yml'):
            print(f'Dispatching pipeline for {path}')
            pipeline(self.configdict, path)
        else:
            print('Non-config File detected. Ignoring...')
