import argparse


class Configuration():

    OPTIONS = (

        # Named Arguments

        (('-v', '--verbose'),
         dict(action='store_true',
              help='Print extra output. This is helpful for debugging.',
              default=False)),

        (('-o', '--output'),
         dict(type=argparse.FileType('w'),
              help='A location to put the results of the conversion. (Defaults to stdout)',
              default='-')),

        (('--verify-specio',),
         dict(action='store_true',
              help=(
                'A convenience utility that validates the input against the Specio '
                'format schema. This does not perform any transformations.'
              ),
              default=False)),

        (('--verify-veripy',),
         dict(action='store_true',
              help=(
                'A convenience utility that validates the input against the Veripy '
                'format schema. This does not perform any transformations.'
              ),
              default=False)),

        # Positional Arguments

        (('input',),
         dict(type=argparse.FileType('r'),
              help='The location of the input file. (To specify stdin use \'-\')')),
    )

    def __init__(self):
        parser = argparse.ArgumentParser()

        for args, kwargs in self.OPTIONS:
            parser.add_argument(*args, **kwargs)

        args = parser.parse_args()
        self.__dict__.update(**vars(args))
