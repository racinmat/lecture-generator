import json

if __name__ == '__main__':
    #name = 'Grek1 - Mahó šódžo včera dnes a zítra-hint-mahó šódžo'
    name = 'Grek1 -  IKEA Záporáci'
    with open('text_out/{}.json'.format(name)) as f:
        data = json.load(f)
    texts = [i['alternatives'][0]['transcript'] for i in data['response']['results']]
    with open('text_out/{}.txt'.format(name), 'w+', encoding='utf-8') as text_file:
        for line in texts:
            text_file.write(line+'\n')
