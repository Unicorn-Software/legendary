from __future__ import annotations

import argparse
import asyncio
import functools
from multiprocessing import freeze_support

from sanic import Sanic, Request, response

from custom import LegendaryCLI

app = Sanic("LegendaryAPI")
api = LegendaryCLI()


class Result:
    status: int
    message: str
    data: dict | list | tuple

    def __init__(self, status: int = 200, message: str = '', data: dict | list | tuple = {}):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        return {'status': self.status, 'message': self.message, 'data': self.data}


async def run_sync(func, *args, **kwargs):
    func = functools.partial(func, *args, **kwargs)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func)


@app.route("/")
async def root(request: Request):
    return response.text('Nothing...')


@app.route("/auth")
async def auth(request: Request):
    return response.json(Result().to_dict())


@app.route("/games")
async def games(request: Request):
    data = await run_sync(api.list_installed)
    return response.json(Result(data=data['data'], message=data['message']).to_dict())


@app.route("/update")
async def update(request: Request):
    return response.json(Result().to_dict())


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
