import vk
from pprint import pprint
from urllib.parse import urlencode, urlparse
import requests
import time
import json
import networkx as nx
import pylab as plt

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
APP_ID = 5954219

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status,video',
    'v': VERSION,
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

token_url = 'https://oauth.vk.com/blank.html#access_token=16b083fc3e686e39fcc1ed743800a42f118cdf8dc2bfdf174ce10eace6784824d4001fc61f91c63678fd1&expires_in=86400&user_id=77847'
o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']

print(access_token)
params = {'access_token': access_token,
          'v': VERSION,
          }

# Получает список друзей пользователя
def get_friends_of_friend(user_id = None):
    if user_id:
        params['user_id'] = user_id
    params['fields'] = 'nickname'
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()

# Получает список моих друзей из ВК
def friendslist_get():
    params['fields'] = 'nickname'
    response = requests.get('https://api.vk.com/method/friends.get', params)

# Возвращает словарь без пользателей, которые удалены или деактивированы
def connections():
    my_friends_list = get_friends_of_friend()
    friends_of_friends = dict()
    for friend in my_friends_list['response']['items']:
        if 'deactivated' not in friend.keys():
            friend_name = friend['first_name'] + ' ' + friend['last_name']
            friends_of_friends[friend_name] = get_friends_of_friend(friend['id'])
        time.sleep(1) # Задержка в секунду, так как ВК не позволяет делать больше 1000 запросов в секунду
    return friends_of_friends

# Записываем полученный список в файл, чтобы не отправлять постоянные запросы в ВК
def list_to_file(list_of_json_friends):
    import json
    with open('friends_list.json','w', encoding = 'utf_8') as friends_file:
        json.dump(list_of_json_friends, friends_file, ensure_ascii=False, indent=2)

# Возвращает отформатированый словарь с пользователями и их друзьями из файла
def open_friends_file():
    with open('friends_list.json', 'r', encoding='utf_8') as f:
        friends = json.load(f)
        friends_treated = dict()
        for account_name, acc_friends in friends.items():
            ids_set = set()
            for user in acc_friends['response']['items']:
                ids_set.add((user['id'], user['first_name'] + ' ' + user['last_name']))
            friends_treated[account_name] = ids_set
    return friends_treated


# Наполняем граф и создаем его графическую модель
def graph_filling(friends_massive):
    g = nx.Graph()
    g_reduced = nx.Graph()
    for connection in friends_massive:
        g.add_edge(*connection)
    g = g.to_undirected()
    # создаем граф, в котором будут только ноды, которые имеют связи с друзьями моих друзей
    for node in g.nodes():
        if g.degree(node) > 1:
            for neighbor in g.neighbors(node):
                if g.degree(neighbor) > 1:
                    g_reduced.add_edge(node, neighbor)
    print('Количество связей между друзьями моих друзей: ', g_reduced.number_of_edges())
    print('Количество друзей моих друзей, имебщих связи с друзьями моих друзей: ', g_reduced.number_of_nodes())
    nx.draw_spectral(g_reduced)
    # nx.draw_networkx(g_reduced,arrows=False,with_labels=False)
    plt.savefig('friends_conn.png', dpi=600)
    plt.close()

# Приводит список из кортежей с друзьями вида (друг, его друг) для наполнения графа
def tuples_for_graph(friends_from_vk):
    cross_for_graph = []
    for friend_name, his_friends in friends_from_vk.items():
        for account in his_friends:
            cross_for_graph.append((friend_name, account[1]))
    print('Количество связей у моих друзей: ', len(cross_for_graph))
    return cross_for_graph


# Выводим на экран информацию о пересечении друзей моих друзей
def print_friends(friends_crossings):
    for crossfriend in friends_crossings:
        print('Друзья {0} и {1} имеют общих друзей {2}' .format(crossfriend[0][0], crossfriend[0][1], crossfriend[1]))

# Находит пересечения друзей между друзьями
def cross_connections(friends_connections):
    crossconnections = set()
    for account_name, ids in friends_connections.items():
        for name, id_search in friends_connections.items():
            crossing = []
            if name != account_name:
                crossing = list(id_search & ids)
            if crossing != []:
                cross_name = ((account_name, name),len(crossing))
                crossconnections.add(cross_name)
    return crossconnections

list_of_connections = connections()
list_to_file(list_of_connections)
friends_from_file = open_friends_file()
# crossings = cross_connections(friends_from_file)
crossings_for_graph = tuples_for_graph(friends_from_file)
graph_filling(crossings_for_graph)