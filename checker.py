import os
import requests
from bs4 import BeautifulSoup
from huey import RedisHuey, crontab
from pushbullet import Pushbullet
from redis import StrictRedis

url = os.getenv('URL', 'https://shop.lego.com/en-CH/Millennium-Falcon-75192')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
pushbullet_api_key = os.getenv('PUSHBULLET_API_KEY', '')

redis = StrictRedis(host=redis_host, port=redis_port, db=redis_db)
huey = RedisHuey('millenium-falcon-checker', host=redis_host, port=redis_port, db=redis_db)
pb = Pushbullet(pushbullet_api_key)


@huey.periodic_task(crontab(minute='*/30'))
def check_status():
    millenium_falcon_response = requests.get(url)
    try:
        millenium_falcon_response.raise_for_status()
        soup = BeautifulSoup(millenium_falcon_response.content, 'html.parser')
        if is_available(soup):
            print(' Millenium Falcon is available')
            send_push_if_necessary("Millenium Falcon Available!!!!", "GET IT NAU")
        elif is_unavailable(soup):
            print('Still out of stock')
            redis.set('millenium-falcon-available', False)
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
    redis_key = 'millenium-falcon-available'
    if not redis.get(redis_key):
        pb.push_note(title, text)
        redis.set(redis_key, True)

