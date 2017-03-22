def check_encoding(news_file):
    import chardet
    rawdata = open(news_file, "rb").read()
    result = chardet.detect(rawdata)
    open(news_file).close()
    return result['encoding']

def search_in_file(sql_file, phrase):
    file_encoding = check_encoding(sql_file)
    with open(sql_file, encoding = file_encoding) as f:
        for string in f:
            if phrase in string.lower():
                return True
        return False

def print_file_path(files_list_to_print):
    from os.path import realpath
    for file in files_list_to_print:
        print(realpath(file))

def take_files(directory):
    import glob
    import os.path
    migrations = directory
    all_sql_files = glob.glob(os.path.join(migrations, "*.sql"))
    return all_sql_files

def iterate_files(files, what_to_find):
    needed_files = []
    for file in files:
        # print(file)
        if search_in_file(file, what_to_find):
            needed_files.append(file)
    return needed_files

def user_input(directory):
    from pprint import pprint
    founded_files = take_files(directory)
    while True:
        phrase_to_find = input('Введите слово или фразу для поиска: ').lower()
        founded_files = iterate_files(founded_files, phrase_to_find)
        print_file_path(founded_files)
        print('Найдено файлов: ', len(founded_files))

choose_dir = int(input('Выберите директорию: 1 - Migrations, 2 - Advanced Mgrations \n'))
if choose_dir == 1:
    user_input('Migrations')
if choose_dir == 2:
    user_input('Advanced Migrations')