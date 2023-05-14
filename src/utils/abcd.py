import codecs
import time
from urllib.parse import quote
from urllib.request import urlopen

from bs4 import BeautifulSoup


def _fetch_html(url: str) -> BeautifulSoup:
    url = quote(url, safe=':/?&=')

    # beautiful soup
    for i in range(5):
        try:
            html = urlopen(url)
            soup = BeautifulSoup(codecs.decode(html.read(), 'utf-8'),
                                 'html.parser')
            if soup.find('form', {'id': 'search-form-index'}):
                print(f"Detected captcha, waiting for 10 seconds...")
                time.sleep(10)
                continue
            return soup

        except Exception as e:
            print(f"Error fetching HTML for `{url}`"
                  f"({i + 1}/5): {e}")

    return None  # noqa


if __name__ == '__main__':
    # url = 'https://openrussian.org/audio-shtooka/американец.mp3'
    # url = 'https://en.openrussian.org/ru/американец'
    url = 'https://en.openrussian.org/ru/аббревиатор'

    # HEAD
    # Translation

    # Usage info *
    # Expressions *

    # Examples

    # Declension *
    # Comparatives *
    # Short forms *
    # Conjugation *
    # Participles *

    # Related words

    html = _fetch_html(url)

    html = html.find('div', {'id': "content"})

    accent = html.find('span').text
    accent = accent if accent != '' else 'None'
    print(accent)

    types = html.find('div', {"class": "overview"}). \
        find_all('p')
    types = [type.text for type in types]
    types = '\n'.join(types)
    types = types if types != '' else 'None'
    print(types)

    tags = html.find('div', {"class": "tags"}). \
        find_all('a')
    tags = [tag.text for tag in tags]
    tags = '\n'.join(tags)
    tags = tags if tags != '' else 'None'
    print(tags)

    trans = html.find('div', {"class": "section translations"}). \
        find_all('div', {"class": "content"})
    trans = [tran.text for tran in trans]
    trans = '\n'.join(trans)
    trans = trans if trans != '' else 'None'
    print(trans)

    ru_sentences = html.find_all('span', {'class': 'ru'})
    ru_sentences = [ru_sentence.text
                    for ru_sentence in ru_sentences]
    # print(ru_sentences)

    tl_sentences = html.find_all('span', {'class': 'tl'})
    tl_sentences = [tl_sentence.text
                    for tl_sentence in tl_sentences]
    # print(tl_sentences)

    sentences = list()
    for ru, tl in zip(ru_sentences, tl_sentences):
        sentences.append(f'{ru} | {tl}')
    sentences = '\n'.join(sentences)
    sentences = sentences if sentences != '' else 'None'
    print(sentences)
