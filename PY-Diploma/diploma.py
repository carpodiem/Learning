import requests
import time
import json
from pprint import pprint

"""
 ЗАДАНИЕ!
 Есть вещи, которые объединяют людей, а есть те, которые делают нас индивидуальными.
 Давайте посмотрим, чем пользователи в ВК не делятся со своими друзьями?
 Задача: Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
 В качестве жертвы, на ком тестировать, можно использовать: 'tim_leary'
"""

# Входные данные
AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.64'
USER_ID = 5030613
USER = 'tim_leary'
TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'

params = {
    'user_id': USER_ID,
    'access_token': TOKEN,
    'v': VERSION,
}


# Запись в JSON файл
def list_to_file(list_of_data, file_name):
    with open(file_name, 'w', encoding='utf_8') as vk_list_file:
        json.dump(list_of_data, vk_list_file, ensure_ascii=False, indent=2)
    print('Записано в файл: ', file_name)


# Получаем список друзей пользователя
def get_friends():
    friends_list = list()
    params['fields'] = 'nickname'
    response = requests.get('https://api.vk.com/method/friends.get', params)
    friends = response.json()['response']['items']
    for friend in friends:
        if 'deactivated' not in friend.keys():
            friends_list.append(friend['id'])
        else:
            if friend['deactivated'] != 'banned' and friend['deactivated'] != 'deleted':
                friends_list.append((friend['id'], friend['first_name'] + ' ' + friend['last_name']))
                # friends_set.add((friend['id'], friend['first_name'] + ' ' + friend['last_name']))
    return friends_list


# Получаем множество групп пользователя
def get_usergroups(user_id=None):
    if user_id:
        params['user_id'] = user_id
    params['extended'] = '1'
    params['fields'] = 'members_count'
    while True:
        try:
            response = requests.get('https://api.vk.com/method/groups.get', params)
            user_groups = response.json()['response']['items']
            groups_count = response.json()['response']['count']
            if groups_count > 1000:
                user_groups = []
                n = (groups_count // 1000) + 1
                for i in range(n):
                    time.sleep(1.3)
                    params['offset'] = i * 1000
                    response = requests.get('https://api.vk.com/method/groups.get', params)
                    user_groups.extend(response.json()['response']['items'])
                print('Больше тысячи: ', len(user_groups))
            break
        except KeyError:
            print('Слишком быстро!')
            time.sleep(2)
    return user_groups, groups_count


# Счетчик, для того, чтобы считать количество друзей, состоящих в той же группе
def counter(json_members):
    count = 0
    for member in json_members:
        count += member['member']
    return count


# Поиск по группам, смотрим с помощью метода groups.isMember, есть ли друг в той же группе, где и целевой пользователь
def is_members(user_groups, user_friends):
    skeleton_groups = []
    params['user_id'] = ''
    n = (len(user_friends) // 200) + 1
    for group in user_groups:
        group_id = group['id']
        params['group_id'] = group_id
        members_count = 0
        if n > 2:
            for i in range(n):
                while True:
                    try:
                        params['user_ids'] = str(user_friends[(i * 200):(i * 200 + 199)])
                        response = requests.get('https://api.vk.com/method/groups.isMember', params)
                        members_count += counter(response.json()['response'])
                        break
                    except KeyError:
                        print('Слишком быстро!')
                        time.sleep(2)
                time.sleep(0.4)
        else:
            params['user_ids'] = user_friends
            response = requests.get('https://api.vk.com/method/groups.isMember', params)
            members_count = counter(response.json()['response'])
        if members_count == 0:
            print('Найдена группа: ', group_id)
            skeleton_groups.append(group_id)
        print('+')
    return skeleton_groups


# Получаем список с сокращенной информацией по группам (ID, имя, количество участников)
def get_group_info(group_ids):
    params['group_ids'] = str(group_ids)
    params['fields'] = 'members_count'
    print(params)
    response = requests.get('https://api.vk.com/method/groups.getById', params)
    groups = response.json()['response']
    groups_info = []
    for group in groups:
        pprint(group['id'])
        groups_info.extend(
            [{
                "id": group['id'],
                "name": group['name'],
                "members_count": group['members_count']
            }]
        )
    pprint(groups_info)
    return groups_info


curr_user_friends = get_friends()

curr_user_groups, curr_groups_count = get_usergroups()
print('Количество групп пользователя: ', curr_groups_count)
list_to_file(curr_user_groups, 'current_groups_list.json')

sk_groups = is_members(curr_user_groups, curr_user_friends)

target_groups = get_group_info(sk_groups)
print(target_groups)
list_to_file(target_groups, 'skeleton_groups_list.json')
print('Группы пользователя, в которых никто из его друзей не состоит, сохранены в файл!')
