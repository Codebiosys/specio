import argparse
import logging


logger = logging.getLogger(__name__)


class Configuration(object):

    OPTIONS = (

        # Named Arguments

        (('-v', '--verbose'),
         dict(action='store_true',
              help='Print extra output. This is helpful for debugging.',
              default=False)),

        (('--patterns',),
         dict(type=str,
              default=None,
              help='Patterns to watch in the path.')),

        (('--ignore_patterns',),
         dict(type=str,
              default=None,
              help='Patterns to ignore in the path.')),

        (('--ignore_directories',),
         dict(action='store_true',
              default=False,
              help='Directories to ignore.')),

        (('--case_sensitive',),
         dict(action='store_true',
              default=False,
              help='Process filenames case sensitivly.')),

        (('--logging_config',),
         dict(type=str,
              default='/app/logging.yml',
              help='A configuration file for logging.')),

        (('-p', '--path',),
         dict(type=str,
              default='/opt/dropzone',
              help='The root of the path to watch.')),

        (('--report-url',),
         dict(type=str,
              default='http://reports:3000/',
              help='The URL to hit for the reports')),

        (('--veripy-features',),
         dict(type=str,
              default='/app/veripy/features/app',
              help='The place to inject features into veripy.')),

        (('-i', '--input',),
         dict(type=str,
              help='The location of the input file. (To specify stdin use \'-\')')),
    )

    def __init__(self):
        logger.debug('Initializing application configuration.')
        parser = argparse.ArgumentParser()

        for args, kwargs in self.OPTIONS:
            parser.add_argument(*args, **kwargs)

        args = parser.parse_args()
        self.__dict__.update(**vars(args))

    def as_dict(self):
        """ Return a dict version of the config that can be sent in a celery task. """
        return self.__dict__
