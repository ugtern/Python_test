from aiohttp import web
from app.db_func import MongoFunc
import json
from jose import jwt


class App:
    def __init__(self, configs):
        self.a = 0
        self.mongo_port = int(configs['port'])
        self.mongo_host = configs['host']

    async def push_data(self, req):

        body = await req.read()
        body = json.loads(body.decode('utf-8'))

        first_var = body.get('one')
        second_var = body.get('two')

        self.a = int(first_var)+int(second_var)

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)
        mongo_db.push_db('Some_title', self.a)

        return web.Response(status=200, text=str(self.a))

    def get_data(self, req):

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)
        posts = mongo_db.take_posts()
        count = len(posts)
        if count > 0:
            last_post = posts[len(posts)-1]
            output_text = 'Заголовок: {}\nТекст: {}\nОбщее количество сообщений в базе: {}'.format(str(last_post['title']), str(last_post['text']), len(posts))
        else:
            output_text = 'Общее количество сообщений в базе: {}'.format(len(posts))

        return web.Response(status=200, text=output_text)

    def delete_data(self, req):

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)
        mongo_db.delete_posts()

        return web.Response(status=200, text='deleted')

    async def reg(self, req):

        body = await req.read()
        body = json.loads(body.decode('utf-8'))

        login = body.get('login')
        password = body.get('password')

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)
        mongo_db.reg_user(login, password)

        return web.Response(status=200, text='Пользователь {} зарегестрирован'.format(login))

    async def auth(self, req):

        body = await req.read()
        body = json.loads(body.decode('utf-8'))

        login = body.get('login')
        password = body.get('password')

        mongo_db = MongoFunc(self.mongo_host, self.mongo_port)
        if mongo_db.auth_user(login, password):
            token = jwt.encode({'client': login+password}, 'secret', algorithm='HS256')
        else:
            token = False

        return web.json_response(status=200, data={'token': token}, headers={
        'Access-Control-Allow-Origin': req.headers['Origin']
        })

        # return web.Response(status=200, text={'token': token}, headers={
        #     'Access-Control-Allow-Origin': req.headers['Origin'],
        #     type: 'json'
        # })

    def get_log(self, req):

        output_text = ''

        with open('log.log') as log:
            for line in log:
                output_text += line

        return web.Response(status=200, text=output_text)
