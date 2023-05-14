import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

import requests
from tqdm import tqdm


def read_tab_delimited_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        lines = file.readlines()
        reader = csv.reader(lines, delimiter='\t')

        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = [executor.submit(row_op, row)
                       for row in reader]
            with tqdm(total=len(lines), unit='word') as pbar:
                for _ in as_completed(futures):
                    pbar.update(1)


def row_op(row):
    id = row[0] if row[0] != '' else 'None'
    position = row[1] if row[1] != '' else 'None'
    bare = row[2] if row[2] != '' else 'None'
    accented = row[3] if row[3] != '' else 'None'
    derived_form = row[4] if row[4] != '' else 'None'
    rank = row[5] if row[5] != '' else 'None'
    disabled = row[6] if row[6] != '' else 'None'
    audio = row[7] if row[7] != '' else 'None'
    usage_en = row[8] if row[8] != '' else 'None'
    usage_de = row[9] if row[9] != '' else 'None'
    number_value = row[10] if row[10] != '' else 'None'
    type = row[11] if row[11] != '' else 'None'
    level = row[12] if row[12] != '' else 'None'

    bare_path = rf'/Users/sjp/Documents/Code/Babel-Tower-of-Anki/resources/datasets/r3/media/{bare}.mp3'
    accented_path = rf'/Users/sjp/Documents/Code/Babel-Tower-of-Anki/resources/datasets/r3/media/{accented}.mp3'

    url = f'https://api.openrussian.org/read/ru/{accented}'
    url = quote(url, safe=':/?&=')
    media = requests.get(url).content
    with open(accented_path, 'wb') as file:
        file.write(media)


# 示例用法
file_path = r'/Users/sjp/Documents/归档/Anki/russian3 - words.csv'
read_tab_delimited_csv(file_path)
