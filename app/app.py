from aiohttp import web
from app.databases import ConnectMongo
import json


class App:
    def __init__(self, configs):
        self.a = 0
        self.mongo_port = int(configs['port'])
        self.mongo_host = configs['host']

    async def connect(self, req):
        mongo_db = ConnectMongo(self.mongo_host, self.mongo_port)

        body = await req.read()
        body = json.loads(body.decode('utf-8'))
        first_var = body.get('one')
        second_var = body.get('two')
        self.a = int(first_var)+int(second_var)

        mongo_db.push_db('Some_title', self.a)

        # for post in posts.find():
        #     print(post)

        return web.Response(status=200, text=str(self.a))

    def make(self, req):
        print(req)
        mongo_db = ConnectMongo(self.mongo_host, self.mongo_port)
        text = mongo_db.take_posts()
        print(text[len(text)-1]['text'])

        return web.Response(status=200, text=str(text[len(text)-1]['text']))
