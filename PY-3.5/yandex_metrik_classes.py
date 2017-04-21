import requests
from pprint import pprint
from urllib.parse import urljoin


APP_ID = '4897d036e1fa4029b38618ceee194ba7'
AUTH_URL = 'https://oauth.yandex.ru/authorize'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

# print('?'.join((AUTH_URL, urlencode(auth_data))))

class YandexBase():
    _TOKEN = 'AQAAAAAKpzb1AAQxfv_b08ESXEFmglNdM-6MCVI'  # полученный токен

    def get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self._TOKEN),
            'User-Agent': 'asdasdasd'
        }


class YandexManagement(YandexBase):
    _MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'

    def counter_list(self):
        url = urljoin(self._MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counters_list = response.json()['counters']
        return counters_list


class YandexCounters(YandexBase):
    _STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'

    def get_count_visits(self, counter_id):
        url = urljoin(self._STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(url, params, headers=headers)
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count

    def get_count_pageviews(self, counter_id):
        url = urljoin(self._STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(url, params, headers=headers)
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count

    def get_count_users(self, counter_id):
        url = urljoin(self._STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(url, params, headers=headers)
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count


management = YandexManagement()
counters = YandexCounters()
pprint(management.counter_list())
print('-----------------------------------')
print('Количество визитов: ', counters.get_count_visits(44132474))
print('-----------------------------------')
print('Количество просмотров: ', counters.get_count_pageviews(44132474))
print('-----------------------------------')
print('Количество пользователей: ', counters.get_count_users(44132474))