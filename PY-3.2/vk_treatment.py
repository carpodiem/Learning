import vk
from pprint import pprint
from urllib.parse import urlencode, urlparse
import requests

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

def get_friends_of_friend(user_id = None):
    if user_id:
        params['user_id'] = user_id
    params['fields'] = 'mickname'
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()

def friendslist_get():
    params['fields'] = 'mickname'
    response = requests.get('https://api.vk.com/method/friends.get', params)
    pprint(response.json())

def connections():
    import time
    my_friends_list = get_friends_of_friend()
    friends_of_friends = dict()
    for friend in my_friends_list['response']['items']:
        if 'deactivated' not in friend.keys():
            pprint(friend)
            friend_name = friend['first_name'] + ' ' + friend['last_name']
            friends_of_friends[friend_name] = get_friends_of_friend(friend['id'])
        time.sleep(1)
    return friends_of_friends

def list_to_file(list_of_json_friends):
    import json
    with open('friends_list.json','w', encoding = 'utf_8') as friends_file:
        json.dump(list_of_json_friends, friends_file, ensure_ascii=False, indent=2)

def open_friends_file():
    import json
    with open('friends_list.json', 'r', encoding='utf_8') as f:
        friends = json.load(f)
    return friends

def cross_checking(accounts_list, my_friends_connections):
    print(type(my_friends_connections))
    print(type(accounts_list))
    for friend_name, friends in my_friends_connections.items():
        crossing = set(friends['response']['items']) & accounts_list
        if  crossing != []:
            print(crossing)
            return_crossing

def cross_connections(friends_connections):
    for account_name, account in friends_connections.items():
        friends = account['response']['items']
        crossed_friends = cross_checking(friends, friends_connections)
        print(crossed_friends)


# def print_friends(friends_of_friends_list):
#     # friends_of_friends_list = friends_of_friends_list.read().decode('cp1251')
#     for friend_name, friend in friends_of_friends_list.items():
#         print('Друзья', friend_name, ':')
#         for friend_of_friend in friend['response']['items']:
#             # pprint(friend['response']['items'])
#             print('   ', friend_of_friend['first_name'], '', friend_of_friend['last_name'], ' ', friend_of_friend['id'])


# list_of_connections = connections()
# list_to_file(list_of_connections)
# print_friends(open_friends_file())
cross_connections(open_friends_file())
