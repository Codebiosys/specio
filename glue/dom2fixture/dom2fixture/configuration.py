import argparse
import sys


class Configuration():

    OPTIONS = (

        # Named Arguments

        (('-v', '--verbose'),
         dict(action='store_true',
              help='Print extra output. This is helpful for debugging.',
              default=False)),

        (('-o', '--output'),
         dict(type=argparse.FileType('w'),
              help='A location to put the results of the extraction. (Defaults to stdout)',
              default=sys.stdout)),

        (('-i', '--input',),
         dict(type=argparse.FileType('r'),
              help='The location of the input file. (Defaults to stdin)',
              default=sys.stdin)),

        (('--url',),
         dict(type=str,
              help='The URL of the given DOM. This will be included in the fixture.',
              default='')),
    )

    def __init__(self):
        parser = argparse.ArgumentParser()

        for args, kwargs in self.OPTIONS:
            parser.add_argument(*args, **kwargs)

        args = parser.parse_args()
        self.__dict__.update(**vars(args))
