# Возвращает словарь с поваренной книгой из файла json
def open_dish_file(file_new):
	import json
	from pprint import pprint 
	with open(file_new, encoding = 'utf_8') as dish_file:
		cook_book = json.load(dish_file)
		# pprint(cook_book)
	return cook_book

# Возвращает словарь с поваренной книгой из файла yaml
def open_dish_yaml_file(file_new):
	import yaml
	from pprint import pprint 
	with open(file_new, encoding = 'utf_8') as yaml_file:
		cook_book = yaml.load(yaml_file)
		# pprint(cook_book)
	return cook_book

# заменяет в файле книгу рецептов книгой с добавленным рецептом
def add_recipe_json(dish_dict_to_add, dish_file):
	import json
	from pprint import pprint
	cook_book = open_dish_file(dish_file)
	for course, dishes in dish_dict_to_add.items():
		for dish, ingredients in dishes.items():
			cook_book['Мамины рецепты'][course][dish] = ingredients
	pprint(cook_book)
	with open(dish_file, 'w', encoding = 'utf_8') as cooking_file:
		json.dump(cook_book, cooking_file, ensure_ascii = False, indent = 2)

# Возвращает словарь со списком только тех блюд, которые мы выбрали
def dishes_compact(dishes, cook_book):
	dishes_list = {}
	for dish in dishes:
		for course in cook_book['Мамины рецепты']:
			dishes_from_book = cook_book['Мамины рецепты'][course]
			if dish in dishes_from_book:
				dishes_list[dish] = dishes_from_book[dish]
	return dishes_list

# Возвращает список с требуемыми покупками
def get_shop_list_by_dishes(dishes_dict_compact, persons_count):
	shop_list = {}
	for dish, ingredients in dishes_dict_compact.items():
		for ingredient in ingredients:
			new_shop_list_item = dict(ingredient)
			new_shop_list_item['quantity'] *= persons_count
			if  new_shop_list_item['ingredient'] not in shop_list:
				shop_list[new_shop_list_item['ingredient']] = new_shop_list_item
				print
			else:
				shop_list[new_shop_list_item['ingredient']]['quantity'] += new_shop_list_item['quantity']
	return shop_list

# Выводит на экран список покупок
def print_shop_list(shop_list):
	print('Требуется купить следующие продукты:')
	for shop_list_item in shop_list.values():
		print('{ingredient:<12} {quantity} {measure}' .format(**shop_list_item))

# Создает список покупок, для работы с файлом JSON
def create_shop_list_json(dishes, persons):
	dishes_dict = dishes_compact(dishes, open_dish_file('dishes.json'))
	shop_list = get_shop_list_by_dishes(dishes_dict, persons)
	print_shop_list(shop_list)
	
# Создает список покупок, для работы с файлом YAML	
def create_shop_list_yaml(dishes, persons):
	dishes_dict = dishes_compact(dishes, open_dish_yaml_file('dishes.yaml'))
	shop_list = get_shop_list_by_dishes(dishes_dict, persons)
	print_shop_list(shop_list)

# Меню для добавления блюда
def user_input():
	persons_count_input = int(input('Введите количество человек: '))
	dishes_input = input('Введите блюда в расчете на одного человека (через запятую):  ').lower().split(', ')
	return dishes_input, persons_count_input

def adding_menu():
	section = input('Введите раздел в Маминых рецептах:  ').lower()
	dish = input('Введите название блюда:  ').lower()
	dish_element = dict()
	dish_element[section] = {dish: []}
	while True:
		ingredient_input = input('Введите ингредиент, количество и меру через пробел:  ').split()
		if ingredient_input == []:
			break
		else: 
			dish_element[section][dish].append(
				{
					'ingredient': ingredient_input[0].lower(), 
					'quantity': ingredient_input[1].lower(), 
					'measure': ingredient_input[2].lower()
				}
			)
	return dish_element
		
# Пользовательское меню
def user_menu(command):
	if command == '1':
		dishes, persons_count = user_input()
		create_shop_list_json(dishes, persons_count)
	elif command == '2':
		dishes, persons_count = user_input()
		create_shop_list_yaml(dishes, persons_count)
	elif command == '3':
		dish_json_file = 'dishes.json'
		dish_to_add = adding_menu()
		add_recipe_json(dish_to_add, dish_json_file)
	elif command == '0':
		print('Пока-пока!')
    
# Стартовое меню
def start_menu():
	start_menu = ''
	while start_menu != '0':
		print('')
		print('------------------------')
		print('Menu')
		print('1 - создать список продуктов из файла json, 2  - создать список продуктов из файла yaml, 3 - добавить рецепт в файл json, 0 - exit')
		start_menu = input('Введите пункт, данные по которому нужно отобразить:')
		print('------------------------')
		user_menu(start_menu)
		
start_menu()