from aiohttp import web
from app.app import App
import logging
import json

main = web.Application()

with open('config.json') as file:
    file = json.load(file)

app = App({'host': file['db_host'], 'port': file['db_port']})

main.router.add_route('POST', '/', app.push_data)
main.router.add_route('GET', '/', app.get_data)
main.router.add_route('GET', '/log/', app.get_log)
web.run_app(main, host=file['host'], port=file['port'])
