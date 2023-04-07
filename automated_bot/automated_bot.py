import json
import logging
import os
import random

import requests
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

fake = Faker()


class AutomatedBot:
    def __init__(self, api_url):
        self.number_of_users = 0
        self.max_posts_per_user = 0
        self.max_likes_per_user = 0
        self.posts = []
        self.users = {}
        self.api_url = api_url
        self.logger = self.configure_logger()

    def load_config(self):
        with open('config.json') as f:
            config_data = json.load(f)
            self.number_of_users = config_data['number_of_users']
            self.max_posts_per_user = config_data['max_posts_per_user']
            self.max_likes_per_user = config_data['max_likes_per_user']

    def configure_logger(self):
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('bot.log')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    def signup_users(self):
        for i in range(self.number_of_users):
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password()

            user_data = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'check_password': password
            }
            headers = {}
            try:
                response = requests.post(f'{self.api_url}/auth/register/', headers=headers, data=user_data)
                data = {
                    'email': email,
                    'password': password
                }

                response = requests.post(f'{self.api_url}/auth/login/', headers=headers, data=data)
                user_id = response.json()['id']
                self.users[user_id] = response.json()['access']
                self.logger.info(f'Created user: {email}: {first_name}, {last_name}.')
            except Exception as exc:
                self.logger.error(f'Error creating user {email}: {first_name} {last_name}. Error message: {exc}')

    def create_posts(self):
        for pk, api_key in self.users.items():
            num_posts = random.randint(1, self.max_posts_per_user)

            for i in range(num_posts):
                headers = {'Authorization': f'Bearer {api_key}'}
                title = fake.unique.text(max_nb_chars=64)
                content = fake.text()
                post_data = {
                    'title': title,
                    'content': content
                }
                try:
                    response = requests.post(
                        f'{self.api_url}/posts/user_posts/',
                        headers=headers,
                        data=post_data
                    )
                    post_id = response.json()['id']
                    self.posts.append(post_id)
                    self.logger.info(f'Created post: {post_id} for User with id {pk}')
                except Exception as exc:
                    self.logger.error(f'Error creating post for User with id {pk}. Error message: {exc}')

    def like_posts(self):
        for pk, api_key in self.users.items():
            num_likes = random.randint(1, self.max_likes_per_user)
            headers = {'Authorization': f'Bearer {api_key}'}

            for i in range(num_likes):
                post_id = random.choice(self.posts)
                response = requests.post(
                    f'{self.api_url}/posts/{post_id}/like/',
                    headers=headers,
                    data=None
                )
                if response.status_code == 201:
                    self.logger.info(f'User {pk} like for post {post_id} created.')
                else:
                    self.logger.error(f'User {pk} like for post {post_id} already exists, skip creation !')

    def run_bot(self):
        self.load_config()
        self.signup_users()
        self.create_posts()
        self.like_posts()


if __name__ == '__main__':
    api_url = os.environ['API_URL']
    bot = AutomatedBot(api_url)
    bot.run_bot()
