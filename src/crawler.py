import codecs
import logging
import re
from urllib.parse import quote
from urllib.request import urlopen

from bs4 import BeautifulSoup

__all__ = ['Crawler']


class Crawler:
    r"""A Crawler.

    Args:
        logger (logging.Logger): A logger to record the crawler's activity.
        max_retries (int, optional): The maximum number of retries for
            fetching a page. Defaults: 5.
        wait_time (int, optional): The waiting time in seconds when a captcha
            is detected. Defaults: 60.
    """

    def __init__(self, logger: logging.Logger,
                 max_retries: int = 5, wait_time: int = 60) -> None:

        self.logger = logger
        self.max_retries = max_retries
        self.wait_time = wait_time

    def _fetch_html(self, index: str) -> BeautifulSoup:
        r"""Fetches the HTML content of a given index.

        Args:
            index (str): The index of the page.

        Returns:
            BeautifulSoup: A BeautifulSoup object containing the parsed HTML
                content, or None if the page cannot be fetched.
        """
        # protect URL
        url = f'https://en.openrussian.org/ru/{index}'
        url = quote(url, safe=':/?&=')

        # beautiful soup
        for i in range(self.max_retries):
            try:
                html = urlopen(url)
                soup = BeautifulSoup(codecs.decode(html.read(), 'utf-8'),
                                     'html.parser')
                # if soup.find('form', {'id': 'search-form-index'}):
                #     self.logger.info(f"Detected captcha, waiting for "
                #                      f"{self.wait_time} seconds...")
                #     time.sleep(self.wait_time)
                #     continue
                return soup

            except Exception as e:
                self.logger.error(f"Error fetching HTML for `{index}`"
                                  f"({i + 1}/{self.max_retries}): {e}")

        return None  # noqa

    def __call__(self, index: str) -> tuple:
        r"""Fetches the data of a given index.

        Args:
            index (str): The index of the page.

        Returns:
            tuple: A tuple containing the word (str), the definition (str), and
                the pronunciation (bytes), or None if the page cannot be
                retrieved.
        """
        soup = self._fetch_html(index)

        if soup is not None:
            html = soup.find('div', {'id': "content"})

            accent = html.find('span').text
            accent = accent if accent != '' else 'None'
            # print(accent)

            types = html.find('div', {"class": "overview"}). \
                find_all('p')
            types = [type.text for type in types]
            types = '\n'.join(types)
            types = types if types != '' else 'None'
            # print(types)

            tags = html.find('div', {"class": "tags"}). \
                find_all('a')
            tags = [tag.text for tag in tags]
            tags = '\n'.join(tags)
            tags = tags if tags != '' else 'None'
            # print(tags)

            trans = html.find('div', {"class": "section translations"}). \
                find_all('div', {"class": "content"})
            trans = [tran.text for tran in trans]
            trans = '\n'.join(trans)
            trans = trans if trans != '' else 'None'
            # print(trans)

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
            # print(sentences)

            return index, accent, types, tags, trans, sentences
        else:
            return None  # noqa


def regex_for_word(word: str) -> str:
    word = re.sub(r'<h2[^>]*>|</h2[^>]*>', '', word)
    word = re.sub(r'<b>|</b>', '`', word)
    word = re.sub(r'\s', '', word)
    return word


def regex_for_exp(exp: str) -> str:
    # TODO 更新对抓取文本的regex
    exp = re.sub(r'<p[^>]*>|</p[^>]*>', '', exp)
    exp = re.sub(r'[\t ]', '', exp)
    exp = re.sub(r'<br/>', '\n', exp)
    exp = re.sub(r'\n+', '\n', exp)
    return exp


if __name__ == '__main__':
    from src.logger import create_logger

    c = Crawler(create_logger('1.log'))
    a = c(r'абзац')
    print(a[0], '\n', a[1])
