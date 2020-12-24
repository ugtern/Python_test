from aiohttp import web
from app.db_func import MongoFunc
import json
from jose import jwt
import pandas as pd
import logging


class App:

    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    def __init__(self, configs):
        self.a = 0
        self.mongo_port = int(configs['port'])
        self.mongo_host = configs['host']
        self.classes = []
        self.df = pd.read_csv('./app/data/train_data_14_december.csv')

        try:
            self.df_valid_data = pd.read_csv('new_data.csv')
        except:
            self.df_valid_data = pd.DataFrame()

    async def get_next_message(self, req):

        body = await req.read()
        body = json.loads(body.decode('utf-8'))

        user_login = body.get('login')

        try:
            df_valid = pd.read_csv('new_data.csv')
            current_id = int(df_valid[df_valid.login == user_login].current_id.max()) + 1
        except:
            current_id = body.get('current_id') or 0

        current_field = self.df[self.df.index == current_id]
        current_message = current_field.message.values[0]

        return web.json_response(status=200, data={'current_message': current_message, 'current_id': current_id}, headers={
        'Access-Control-Allow-Origin': req.headers['Origin']
        })

    async def set_correct_class(self, req):

        body = await req.read()
        body = json.loads(body.decode('utf-8'))

        user_login = body.get('login')
        correct_class = body.get('correct_class')
        current_id = body.get('current_id')

        current_field = self.df[self.df.index == current_id]
        current_message = current_field.message.values[0]

        self.df_valid_data = self.df_valid_data.append(pd.DataFrame({'current_id': [current_id],
                                                                     'login': [user_login],
                                                                     'message': [current_message],
                                                                     'class': [correct_class]}), ignore_index=True)

        self.df_valid_data.to_csv('new_data.csv')

        current_id += 1

        return web.json_response(status=200, data={'current_id': current_id}, headers={
        'Access-Control-Allow-Origin': req.headers['Origin']
        })

    async def get_classes(self, req):

        classes = list(self.df.label.unique())

        logging.info(classes)

        self.classes = classes

        return web.json_response(status=200, data={'classes': classes}, headers={
        'Access-Control-Allow-Origin': req.headers['Origin']
        })

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

    def get_log(self, req):

        output_text = ''

        with open('log.log') as log:
            for line in log:
                output_text += line

        return web.Response(status=200, text=output_text)
