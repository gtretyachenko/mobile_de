# -*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup
import sys


params = {'page': 1}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
pages = params['page']

url = 'https://www.mobile.de/ru/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/mercedes-benz-glc-220-d/vhc:car,srt:price,sro:asc,ms1:17200_253_d,frn:2017,frx:2019,ful:hybrid_diesel!diesel!lpg,mlx:125000'
if len(sys.argv) > 1:
    url = sys.argv[1]

if url.find('pgn:') == -1:
    halfs_url = url.split('vhc:car')
    url = halfs_url[0] + 'pgn:1' + halfs_url[1]

val_pgs = 10
if len(url.split('pgs:')) > 1:
    val_pgs = int(url.split('pgs:')[1][0:1])

response = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='search-result-header g-col-12 js-search-result-header hidden-print')

count_items = 0
for n, i in enumerate(items, start=1):
    count_items = i.find('h1', class_='h2 u-text-orange').text
    count_items = int(count_items.replace(chr(160), '').split()[0])
    if count_items > 0:
        break

res = []
res_res = []
count = 0
pages = int(count_items / val_pgs) + 1
while params['page'] <= pages:
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='g-row js-ad-entry')
    for n, i in enumerate(items, start=1):
        count += 1
        res.append([params['page']])
        res[count - 1].append(n)
        if i.find('h3', class_='vehicle-title g-col-12 u-text-nowrap'):
            item_name = i.find('h3', class_='vehicle-title g-col-12 u-text-nowrap').text
            item_name = item_name.replace('Новое', 'Новое,')
            if item_name.split(',')[0] == 'Новое':
                res[count - 1].append(item_name.split(',')[0])
                res[count - 1].append(item_name.split(',')[1])
            else:
                res[count - 1].append('-')
                res[count - 1].append(item_name.split(',')[0])
        else:
            res[count - 1].append('-')
            res[count - 1].append('-')
        if i.find('div', class_='dealer-ratings'):
            item_name = i.find('div', class_='dealer-ratings').text
            res[count - 1].append(item_name.split('★')[0])
            res[count - 1].append(item_name.split('★')[1][1:-1])
        else:
            res[count - 1].append(0)
            res[count - 1].append(0)
        if i.find('div', class_='vehicle-information g-col-s-6 g-col-m-8'):
            item_name = i.find('div', class_='vehicle-information g-col-s-6 g-col-m-8').text
            res[count - 1].append(item_name.split(',')[0])
            res[count - 1].append(item_name.replace('км', ',').split(',')[1][1:-1].replace(chr(160), ''))
        else:
            res[count - 1].append('-')
            res[count - 1].append(0)
        if i.find('div', class_='g-col-s-6 g-col-m-4 u-text-right'):
            ii = i.find('div', class_='g-col-s-6 g-col-m-4 u-text-right')
            item_name = ii.find('div', class_='vehicle-prices').contents[0].text
            item_name = item_name.replace(chr(160), '')
            res[count - 1].append(int(item_name.split('€')[0]))
            # res[count - 1].append(item_name.split('€')[1][2:-1])
            if len(ii.find('div', class_='vehicle-prices').contents) > 1:
                item_name = ii.find('div', class_='vehicle-prices').contents[1].text
                item_name = item_name.replace(chr(160), '')
                res[count - 1].append(int(item_name.split('€')[0]))
            else:
                res[count - 1].append(int(item_name.split('€')[0]))
            # link_to_entry = 'https://www.mobile.de' + i.find('a').get('href')
            # response = requests.get(link_to_entry, params=params, headers=headers)
            # soup = BeautifulSoup(response.text, 'lxml')
            # items_items = soup.find('div', class_='vip-details-block u-margin-bottom-18')
            # res_res.append([params['page']])
            # res_res[count - 1].append(n)
            # for t, iii in enumerate(items_items.find('div', class_='attributes-box g-col-12')):
            #     cont = iii.contents[1].text
            #     if t == 5:
            #         cont = cont.replace('км', '').replace(chr(160), '')
            #     res_res[count - 1].append(cont)
            # for t, iii in enumerate(items_items.find('div', class_='further-tec-data g-col-12')):
            #     cont = iii.contents[1].text
            #     if t == 0:
            #         cont = cont.replace('ссм', '').replace(chr(160), '')
            #     res_res[count - 1].append(cont)


        print(res[count - 1])
        # print(res_res[count - 1])
    num_page = params['page']
    url = url.replace(f'pgn:{num_page}', f'pgn:{num_page+1}')
    params['page'] += 1

myData = res
# myData2 = res_res
with open('C:/Users/Admin/PycharmProjects/mobile_de/data_result.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['NumPage', 'NumLot', 'MarkerNew', 'LotName', 'ShopRating', 'CountReviews',
        'Born(mm/yyyy)', 'ODO km', 'PriceEur', 'NetPriceEur']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer = csv.writer(csvfile)
    writer.writerows(myData)
    print("Writing complete")

# with open('C:/Users/Admin/PycharmProjects/mobile_de/data_result2.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     fieldnames = ['Состояние', 'Категория', 'Год выпуска', 'Коробка передач', 'Топливо', 'Пробег',
#         'Мощность', 'Объем двигателя', 'Кол-во мест', 'Кол-во дверей', 'Класс эко', 'Кол-во влад',
#                   'Общий осмотр', 'Цвет', 'Состояние2', 'Категория', 'Номер ТС', 'Датчики парковки', 'Дизаин салон']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer = csv.writer(csvfile)
#     writer.writerows(myData2)
#     print("Writing complete")
