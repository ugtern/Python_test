from pymongo import MongoClient
import datetime


class ConnectMongo:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_db(self):
        client = MongoClient(self.host, self.port)
        return client.test

    def get_posts(self):
        db = self.get_db()
        return db.posts

    def push_db(self, title, text):
        posts = self.get_posts()
        post = {
            'title': title,
            'text': text,
            'date': datetime.datetime.now()
        }
        posts.insert_one(post)

    def take_posts(self):
        posts = self.get_posts()
        return [post for post in posts.find()]

# print(db)
#
# post = {
#     'author': 'test',
#     'test': 'test massage',
#     'tags': ['tag_1', 'next_some_tag', 'taggester'],
#     'date': datetime.datetime.now()
# }
#
# posts = db.posts
# post_id = posts.insert_one(post).inserted_id
# print(post_id)
#
# # print(posts.find_one({'author': 'test'}))
#
# for post in posts.find():
#     print(post)
#
# print(posts.count())
