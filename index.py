from aiohttp import web
from app.app import App
import logging
import json

main = web.Application()

with open('config.json') as file:
    file = json.load(file)

app = App({'host': file['db_host'], 'port': file['db_port']})

main.router.add_route('POST', '/reg/', app.reg)
main.router.add_route('POST', '/auth/', app.auth)

main.router.add_route('POST', '/', app.push_data)
main.router.add_route('GET', '/', app.get_data)

main.router.add_route('GET', '/log/', app.get_log)
main.router.add_route('DELETE', '/del/', app.delete_data)

main.router.add_route('GET', '/get_classes/', app.get_classes)

main.router.add_route('POST', '/get_next_message/', app.get_next_message)
main.router.add_route('POST', '/set_correct_class/', app.set_correct_class)

web.run_app(main, host=file['host'], port=file['port'])
