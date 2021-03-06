from app.databases import ConnectMongo
import datetime
import logging


class MongoFunc(ConnectMongo):

    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    def __init__(self, host, port):
        super().__init__(host, port)

    def push_db(self, title, text):

        posts = self.get_posts()

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post = {
            'title': title,
            'text': text,
            'date': now
        }

        try:
            posts.insert_one(post)
        except:
            logging.error('Неудалось записать данные в бд')
        else:
            logging.info('пост {} был записан в монго в {}'.format(post['title'], now))

    def delete_posts(self):

        posts = self.get_posts()
        posts.delete_many({})

    def take_posts(self):
        posts = self.get_posts()
        return [post for post in posts.find()]

    def reg_user(self, login, password):

        user = {'login': login, 'password': password}

        users = self.get_users()
        try:
            users.insert_one(user)
        except:
            logging.error('Неполучилось создать пользователя')
        else:
            logging.info('Пользователь сохранен')

    def auth_user(self, login, password):
        users = self.get_users()
        return True if [user for user in users.find_one({'login': login, 'password': password})] else False
