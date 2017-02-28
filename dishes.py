
cook_book = {
  'яичница': [
    {'ingredient_name':'яйца', 'quantity': 2, 'measure': 'шт.'},
    {'ingredient_name':'помидоры', 'quantity': 100, 'measure': 'гр.'}
    ],
  'стейк': [
    {'ingredient_name':'мясо', 'quantity': 300, 'measure': 'гр.'},
    {'ingredient_name':'специи', 'quantity': 5, 'measure': 'гр.'},
    {'ingredient_name':'масло', 'quantity': 10, 'measure': 'мл.'}
    ],
  'салат': [
    {'ingredient_name':'огурцы', 'quantity': 100, 'measure': 'гр.'},
    {'ingredient_name':'помидоры', 'quantity': 100, 'measure': 'гр.'},
    {'ingredient_name':'масло', 'quantity': 100, 'measure': 'мл.'},
    {'ingredient_name':'лук', 'quantity': 1, 'measure': 'шт.'}
    ]
  }
  
def get_shop_list_by_dishes(dishes, persons_count):
  shop_list = {}
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
  # for shop_list_item in shop_list.values():
  #   print('{0} {1} {2:>20}' .format(shop_list_item['ingredient_name'], shop_list_item['quantity'], shop_list_item['measure']))
  for shop_list_item in shop_list.values():
    print('{ingredient_name} {quantity} {measure}' .format(**shop_list_item))
    
def creat_shop_list():
  persons_count = int(input('Введите количество человек'))
  dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
  shop_list = get_shop_list_by_dishes(dishes,persons_count)
  print_shop_list(shop_list)
  
creat_shop_list()
