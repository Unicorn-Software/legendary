import argparse
from multiprocessing import freeze_support

from sanic import Sanic, Request, response

app = Sanic("LegendaryAPI")


@app.route("/")
async def test(request: Request):
    return response.text('Nothing...')


@app.route("/auth")
async def test(request: Request):
    return response.json({})


def main(_app: Sanic):
    parser = argparse.ArgumentParser(description=f'LegendaryAPI v0.1.0')
    # parser.register('action', 'parsers', HiddenAliasSubparsersAction)
    parser.add_argument('--host', dest='host', action='store', metavar='<IP or domain>',
                        default='localhost', help='Host for API server (default: %(default)s)')
    parser.add_argument('-p', '--port', dest='port', action='store', metavar='<integer>',
                        default=8845, help='Port for API server (default: %(default)s)')

    args, extra = parser.parse_known_args()

    _app.run(host=args.host, port=args.port)


if __name__ == '__main__':
    # required for pyinstaller on Windows, does nothing on other platforms.
    freeze_support()
    main(app)
