""" Run Api with gunicorn config
"""
import sys
import gunicorn
from .app import main


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """ Stand Alone Application
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """ load config
        """
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """ load
        """
        return self.application

    def init(self, parser, opts, args):
        """ init
        """


# Exit codes that will be returned with its error message
EXIT_CODES = {
    -5: "Incorrect bind format, example: --bind=127.0.0.1:5000",
    -6: "Incorrect workers format, example: --workers=4"
}


def make_table() -> str:
    """
        Makes a table because why not?
    """
    print(f'┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print(f'┃Code\t ┃ Description')
    print(f'┣━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    for key, value in EXIT_CODES.items():
        print(f'┃{key:03}\t ┃ {value}')
    print(f'┗━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')


def handel_user_arguments() -> dict:
    """
        Parsed console arguments and passes them into application
    """
    bind = '127.0.0. 1:5000'
    workers = 4
    for arg in sys.argv:
        if arg.startswith('--bind='):
            parts = arg.split('=')
            if len(parts) < 2:
                print(EXIT_CODES[-5], file=sys.stderr)
                sys.exit(-5)
            bind = parts[1]

        if arg.startswith('--workers='):
            if len(parts) < 2:
                print(EXIT_CODES[-5], file=sys.stderr)
                sys.exit(-5)
        if arg.startswith('--codes') or arg.startswith('--help'):

            make_table()
        if arg.startswith('--no-start') or arg.startswith('--help'):
            sys.exit(0)
    return {
        'bind': bind,
        'workers': workers,
    }


def run_application():
    """
        Runs the StandaloneApplication of gunicorn
    """
    StandaloneApplication(
        main(UNIT_TEST=False),
        options=handel_user_arguments()
    ).run()


if __name__ == '__main__':
    run_application()
