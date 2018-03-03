import os

import pickle
import requests
from bs4 import BeautifulSoup
from huey import RedisHuey, crontab
from pushbullet import Pushbullet
from redis import StrictRedis, BlockingConnectionPool

url = os.getenv('URL', 'https://shop.lego.com/en-CH/Millennium-Falcon-75192')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
pushbullet_api_key = os.getenv('PUSHBULLET_API_KEY', '')

pool = BlockingConnectionPool(host=redis_host, port=redis_port, db=redis_db)
redis = StrictRedis(connection_pool=pool)
huey = RedisHuey('millennium-falcon-checker', connection_pool=pool)
pb = Pushbullet(pushbullet_api_key)


@huey.periodic_task(crontab(minute='*/30'))
def check_status_task():
    check_status()


def check_status():
    millennium_falcon_response = requests.get(url)
    try:
        millennium_falcon_response.raise_for_status()
        soup = BeautifulSoup(millennium_falcon_response.content, 'html.parser')
        if is_available(soup):
            print(' Millennium Falcon is available')
            send_push_if_necessary("Millennium Falcon Available!!!!", "GET IT NAU")
        elif is_unavailable(soup):
            print('Still out of stock')
            redis.set('millennium-falcon-available', pickle.dumps(False))
        else:
            print('Something changed you better have a look.')
            send_push_if_necessary('Something changed in the LEGO Shop')
    except requests.RequestException:
        print('I have a bad feeling about this')


def is_available(soup):
    return soup.find('div', {"class":"available--now"}) is not None


def is_unavailable(soup):
    return soup.find('div', {"class": "available--never"}) is not None


def send_push_if_necessary(title, text=''):
    redis_key = 'millennium-falcon-available'
    if not pickle.loads(redis.get(redis_key)):
        pb.push_note(title, text)
        redis.set(redis_key, pickle.dumps(True))


if __name__ == '__main__':
    check_status()
