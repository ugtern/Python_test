from aiohttp import web
from app.db_func import MongoFunc
import json


class App:
    def __init__(self, configs):
        self.a = 0
        self.mongo_port = int(configs['port'])
        self.mongo_host = configs['host']

    async def push_data(self, req):

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)

        body = await req.read()
        body = json.loads(body.decode('utf-8'))

        first_var = body.get('one')
        second_var = body.get('two')

        self.a = int(first_var)+int(second_var)

        mongo_db.push_db('Some_title', self.a)

        return web.Response(status=200, text=str(self.a))

    def get_data(self, req):

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)
        posts = mongo_db.take_posts()
        last_post = posts[len(posts)-1]
        output_text = 'Заголовок: {}\nТекст: {}\nОбщее количество сообщений в базе: {}'.format(str(last_post['title']), str(last_post['text']), len(posts))

        return web.Response(status=200, text=output_text)

    def delete_data(self, req):

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)


    def get_log(self, req):

        output_text = ''

        with open('log.log') as log:
            for line in log:
                output_text += line

        return web.Response(status=200, text=output_text)
