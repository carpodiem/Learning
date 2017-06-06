import requests
import time
import json
from pprint import pprint
import progressbar as pb

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

pool = requests.Session()

"""
Функция записи в JSON файл
"""


def list_to_file(list_of_data, file_name):
    with open(file_name, 'w', encoding='utf_8') as vk_list_file:
        json.dump(list_of_data, vk_list_file, ensure_ascii=False, indent=2)
    print('Записано в файл: ', file_name)


"""
Добавили функцию для запросов к VK.
В качестве параметров принимает параметры для запроса и имя метода (по-умолчанию, isMember)
"""


def vk_request(parameters, vk_method='groups.isMember'):
    pool.params = parameters
    url = 'https://api.vk.com/method/' + vk_method
    while True:
        response = pool.get(url)
        if response.ok:
            return response
        else:
            time.sleep(2)


"""
Получаем список друзей пользователя
"""


def get_friends():
    friends_list = list()
    params['fields'] = 'nickname'
    friends = vk_request(params, 'friends.get').json()['response']['items']
    for friend in friends:
        if 'deactivated' not in friend.keys():
            friends_list.append(friend['id'])
        else:
            if friend['deactivated'] != 'banned' and friend['deactivated'] != 'deleted':
                friends_list.append((friend['id'], friend['first_name'] + ' ' + friend['last_name']))
                # friends_set.add((friend['id'], friend['first_name'] + ' ' + friend['last_name']))
    return friends_list


"""
Получаем множество групп пользователя. 
Оптимизировали ошибки 
"""


def get_usergroups(user_id=None):
    if user_id:
        params['user_id'] = user_id
    params['extended'] = '1'
    params['fields'] = 'members_count'
    response = vk_request(params, 'groups.get')
    user_groups = response.json()['response']['items']
    groups_count = response.json()['response']['count']
    if groups_count > 1000:
        user_groups = []
        n = (groups_count // 1000) + 1
        for i in range(n):
            time.sleep(1.3)
            params['offset'] = i * 1000
            user_groups.extend(
                vk_request(params, 'groups.get').json()['response']['items']
            )
        print('Больше тысячи: ', len(user_groups))
    return user_groups, groups_count


"""
Счетчик, для того, чтобы считать количество друзей, состоящих в той же группе
"""


def counter(json_members):
    count = 0
    for member in json_members:
        count += member['member']
    return count


"""
Поиск по группам, смотрим с помощью метода groups.isMember, есть ли друг в той же группе, где и целевой пользователь
"""


def is_members(user_groups, user_friends, friends_q):
    skeleton_groups = []
    params['user_id'] = ''
    n = (len(user_friends) // 200) + 1
    with pb.ProgressBar(max_value=len(user_groups), widgets=[
        ' [', pb.Timer('Прошло времени: %(elapsed)s'), '] ',
        '[', pb.SimpleProgress(), '] ',
        pb.Bar(),
        ' (', pb.ETA(
            format_not_started='Оставшееся время: --:--:--',
            format_zero='Оставшееся время: 00:00:00',
            format='Оставшееся время: %(eta)s'
        ), ') ', ' ' * 40
    ]) as bar:
        for t, group in enumerate(user_groups):
            group_id = group['id']
            params['group_id'] = group_id
            members_count = 0
            if n > 2:
                for i in range(n):
                    while True:
                        try:
                            params['user_ids'] = str(user_friends[(i * 200):(i * 200 + 199)])
                            members_count += counter(vk_request(params).json()['response'])
                            break
                        except KeyError:
                            time.sleep(2)
                    time.sleep(0.4)
            else:
                params['user_ids'] = user_friends
                members_count = counter(vk_request(params).json()['response'])
            if members_count <= friends_q:
                skeleton_groups.append(group_id)
            bar.update(t)
    return skeleton_groups


"""
Получаем список с сокращенной информацией по группам (ID, имя, количество участников)
"""


def get_group_info(group_ids):
    params['group_ids'] = str(group_ids)
    params['fields'] = 'members_count'
    groups = vk_request(params, 'groups.getById').json()['response']
    groups_info = []
    for group in groups:
        groups_info.extend(
            [{
                "id": group['id'],
                "name": group['name'],
                "members_count": group['members_count']
            }]
        )
    return groups_info


"""
Функция, запускающая последовательность функций для получения результата.
"""

def process_func(n):
    curr_user_friends = get_friends()
    curr_user_groups, curr_groups_count = get_usergroups()
    print('Количество групп пользователя: ', curr_groups_count)
    list_to_file(curr_user_groups, 'current_groups_list.json')
    print('')
    sk_groups = is_members(curr_user_groups, curr_user_friends, n)
    target_groups = get_group_info(sk_groups)
    print('')
    print('Найдено {} групп'.format(len(target_groups)))
    print('-' * 30)
    print('Искомые группы:')
    pprint(target_groups)
    print('-' * 30)
    list_to_file(target_groups, 'skeleton_groups_list.json')
    print('Группы пользователя, в которых никто из его друзей не состоит, сохранены в файл!')


"""
Главная функция запуска
"""


def main():
    print(
        'Введите количество друзей, '
        'которые также могут состоять в одних группах с пользователем'
        ', не более чем это количество.'
    )
    friends_q = input('(По-умолчанию - 0). Количество друзей = ')
    if friends_q == '':
        friends_q = 0
    process_func(int(friends_q))


if __name__ == '__main__':
    main()
