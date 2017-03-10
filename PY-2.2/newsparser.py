def frequent_10(dict_numbered):
	dict_freq = dict()
	for _ in range(10):
		max_repeated = 0
		key_freq = '' 
		for key in dict_numbered:
			if dict_numbered[key] > max_repeated:
				max_repeated = dict_numbered[key]
				key_freq = key
			# elif dict_numbered[key] = max_repeated:
				# key_freq = [key_freq, key]
		dict_freq[key_freq] = max_repeated
		dict_numbered[key_freq] = 0
	return dict_freq

def frequent_words(words_list):
	words_dictionary = dict()
	for word in words_list:
		if word in words_dictionary:
			words_dictionary[word] += 1
		else:
			words_dictionary[word] = 1
	return words_dictionary
	
def words_obtaining(news_text):
	symbols_to_strip = "0123456789 !@#$%^&*()-_+={}[]|\:;'<>?,./\""
	new_output = []
	for word in news_text.split():
		word_new = word.strip('<br>')
		if word_new[0:4] == 'href':
			word_new = word_new.split('>')[1].strip('</a')		
		word_new = word_new.strip(symbols_to_strip)
		new_output.append(word_new)
	for word in new_output:
		if '<br>' in word:
			words_br = word_new.split('<br><br>')
			new_output.remove(word)
			new_output += words_br
	output = []
	for word in new_output:
		word_new = word.strip(symbols_to_strip)
		if len(word_new) > 6:
			output.append(word_new.lower())
	return sorted(output)

def check_encoding(news_file):
	import chardet
	rawdata = open(news_file, "rb").read()
	result = chardet.detect(rawdata)
	open(news_file).close()
	return result['encoding']
	
def file_open(filename, charset):
	import json
	from pprint import pprint
	with open (filename, encoding = charset) as newsfile:
		news = json.load(newsfile)
		news_quantity = len(news['rss']['channel']['item'])
		all_words = []
		for i in range(news_quantity):
			all_words += words_obtaining(news['rss']['channel']['item'][i]['description']['__cdata'])
		# print('')
		# print('')
		# print(all_words)
		# print('')
		# print('')
		# print(frequent_words(all_words))
		# print('')
		# print('')
		freq_10 = frequent_10(frequent_words(all_words))
		print('Топ 10 самых часто встречаемых слов длинее 6 символов:')
		for word in freq_10:
			spaces = 20 - len(word)
			print('  ',word,' ' * spaces,freq_10[word])

def file_open_format2(filename, charset):
	import json
	from pprint import pprint
	with open (filename, encoding = charset) as newsfile:
		news = json.load(newsfile)
		news_quantity = len(news['rss']['channel']['item'])
		all_words = []
		for i in range(news_quantity):
			all_words += words_obtaining(news['rss']['channel']['item'][i]['description'])
		# print('')
		# print('')
		# print(all_words)
		# print('')
		# print('')
		# print(frequent_words(all_words))
		# print('')
		# print('')
		freq_10 = frequent_10(frequent_words(all_words))
		print('Топ 10 самых часто встречаемых слов длинее 6 символов:')
		for word in freq_10:
			spaces = 20 - len(word)
			print('  ',word,' ' * spaces,freq_10[word])
	

		
file_open('newsafr.json', check_encoding('newsafr.json'))
file_open('newscy.json', 'koi8_r')
file_open('newsfr.json',  check_encoding('newsfr.json'))
file_open_format2('newsit.json', check_encoding('newsit.json'))
