import requests

API_KEY = 'trnsl.1.1.20170403T134942Z.3fef2d2b4f4b3acc.a28d26b110a85483ca1cc8d970b513d687a1f71a'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def translate_it(text_file, target_file, from_lang, to_lang='ru'):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ? 
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
     
    :param to_lang: 
    :return: 
    """
    with open(text_file, 'r', encoding='utf_8') as translate_file:
        text =[]
        for line in translate_file:

            params = {
                'key': API_KEY,
                'text': line,
                'lang': '{0}-{1}' .format(from_lang, to_lang),
            }
            response = requests.get(URL, params=params)
            json_ = response.json()
            text.append(' '.join(json_['text']))

    with open(target_file, 'w', encoding='utf_8') as translated_f:
        translated_f.writelines(text)


translate_it('D:\Project\GitHub\Learning\PY-3.3\hw_news\DE.txt', 'DE_translated.txt', 'de')
translate_it('D:\Project\GitHub\Learning\PY-3.3\hw_news\ES.txt', 'ES_translated.txt', 'es')
translate_it('D:\Project\GitHub\Learning\PY-3.3\hw_news\FR.txt', 'FR_translated.txt', 'fr')