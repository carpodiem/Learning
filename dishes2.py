def read_file():
	cook_book = dict()
	with open ('dishes.txt', encoding = 'utf-8') as f:
		while True:
			ingredients = []
			dish = f.readline().strip()
			cook_book[dish] = []
			ingredients_count = int(f.readline().strip())
			for _ in range(ingredients_count):
				ingredient = f.readline().strip().split(' | ')
				cook_book[dish].append({'ingredient_name':ingredient[0], 'quantity': int(ingredient[1]), 'measure': ingredient[2]})
			line = f.readline()
			if line == '':
				break
	return cook_book
	
def get_shop_list_by_dishes(dishes, persons_count):
  shop_list = {}
  cook_book = read_file()
  for dish in dishes:
    for ingredient in cook_book[dish]:
      new_shop_list_item = dict(ingredient)
      new_shop_list_item['quantity'] *= persons_count
      if  new_shop_list_item['ingredient_name'] not in shop_list:
        shop_list[new_shop_list_item['ingredient_name']] = new_shop_list_item
      else:
        shop_list[new_shop_list_item['ingredient_name']]['quantity'] += new_shop_list_item['quantity']
  return shop_list

def print_shop_list(shop_list):
  for shop_list_item in shop_list.values():
    print('{ingredient_name} {quantity} {measure}' .format(**shop_list_item))
    
def create_shop_list():
  persons_count = int(input('Введите количество человек: '))
  dishes = input('Введите блюда в расчете на одного человека (через запятую):  ').lower().split(', ')
  shop_list = get_shop_list_by_dishes(dishes,persons_count)
  print_shop_list(shop_list)
 
create_shop_list()