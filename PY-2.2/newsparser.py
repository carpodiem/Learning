# функция определяет 10 или более самых повторяющихся слов
def frequent_10(list_words):
    frequent_10words = dict()
    for i in range(0, 10):
        word = list_words[i][0]
        quantity = list_words[i][1]
        frequent_10words[word] = quantity
    n = 10
    while list_words[10][1] == list_words[n + 1][1]:
        n += 1
        word = list_words[n][0]
        quantity = list_words[n][1]
        frequent_10words[word] = quantity
    # Если выводится больше 10-ти слов, значит 10е слово в списке повторяется столько же раз,
    # сколько и последующие несколько слов
    print('Топ ', len(frequent_10words), ' самых часто встречаемых слов длинее 6 символов:')
    return frequent_10words


# функция требуется для сортировки списка по длине слова
def sort_by_length(input_str):
    return len(input_str)


# функция составляет список кортежей со словами отсортированными по длине,
# кортежи отсортированы по количеству повторений, с указанием количеством повторений
def frequent_words(all_words_list):
    words_dictionary = dict()
    all_words_list = sorted(all_words_list, key=sort_by_length, reverse=True)
    for word in all_words_list:
        if len(word) <= 6:
            break
        if word in words_dictionary:
            words_dictionary[word] += 1
        else:
            words_dictionary[word] = 1
    frequent_words_result = sorted(words_dictionary.items(), key=lambda x: x[1], reverse=True)
    # Выдает список кортежей, состоящих из слова и количества его повторений.
    # Список отсортирован по количеству повторений в кортежах от большего к меньшему
    return frequent_words_result


# Функция вычленяет слова из новости и удаляет ненужные символы
def words_obtaining(news_text):
    symbols_to_strip = "0123456789 !@#$%^&*()-_+={}[]|\:;'<>?,./\"»«"
    filtered_words = []
    for word in news_text.split():
        word_new = word.strip('<br>')
        if word_new[0:4] == 'href':
            word_new = word_new.split('>')[1].strip('</a')
        if '<br><br>' not in word_new:
            word_new = word_new.strip(symbols_to_strip)
            filtered_words.append(word_new)
        else:
            words_br = word_new.split('<br><br>')
            filtered_words.append(words_br[0].strip(symbols_to_strip))
            filtered_words.append(words_br[1].strip(symbols_to_strip))
    return sorted(filtered_words)


# Определяет кодировку файла
def check_encoding(news_file):
    import chardet
    rawdata = open(news_file, "rb").read()
    result = chardet.detect(rawdata)
    open(news_file).close()
    return result['encoding']


# Функция для работы с файлами одного формата
def file_open(filename, charset):
    import json
    with open(filename, encoding=charset) as newsfile:
        news = json.load(newsfile)
        news_quantity = len(news['rss']['channel']['item'])
        all_words = []
        for i in range(news_quantity):
            # Проверка того, какой тип файла открыт (со словарем в поле description или без)
            if isinstance(news['rss']['channel']['item'][i]['description'], dict):
                all_words += words_obtaining(news['rss']['channel']['item'][i]['description']['__cdata'])
            else:
                all_words += words_obtaining(news['rss']['channel']['item'][i]['description'])
        freq_10 = frequent_10(frequent_words(all_words))
        # Сортировка словаря в кортеж со значениями по убыванию
        frequent10 = sorted(freq_10.items(), key=lambda x: x[1], reverse=True)
        print('Исследуем файл с новостями ', filename)
        print('   Слово', ' ' * 13, '|', 'Кол-во повторов')
        print('-' * 40)
        for word in frequent10:
            spaces = 18 - len(word[0])
            print('  ', word[0], ' ' * spaces, '|', word[1])
        print('-' * 40)
        print('')


file_open('newsafr.json', check_encoding('newsafr.json'))
file_open('newscy.json', 'koi8_r')
file_open('newsfr.json', check_encoding('newsfr.json'))
file_open('newsit.json', check_encoding('newsit.json'))
