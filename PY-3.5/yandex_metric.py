import requests
from urllib.parse import urlencode, urlparse, urljoin


APP_ID = '4897d036e1fa4029b38618ceee194ba7'
AUTH_URL = 'https://oauth.yandex.ru/authorize'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

# print('?'.join((AUTH_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAKpzb1AAQxfv_b08ESXEFmglNdM-6MCVI' # получили токен

class YandexMetric(object):
