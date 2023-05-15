import argparse
import os
import re

from src import create_logger, Encoder, NoteTemplate


########################################
# Chinese -> Russian
########################################


# class Chinese2RussianNoteTemplate(NoteTemplate):
#     def __init__(self,
#                  template_id=1001,
#                  template_name='BabelTowerNote',
#                  fields: tuple = ('单词',
#                                   '发音',
#                                   '千亿释义',
#                                   'AI释义',
#                                   '笔记'),
#                  front_format='formats/russian/chinese2russian/front.html',
#                  back_format='formats/russian/chinese2russian/back.html',
#                  css_format='formats/russian/chinese2russian/style.css'):
#         super().__init__(template_id, template_name, fields,
#                          front_format, back_format, css_format)
#
#
# class Chinese2RussianEncoder(Encoder):
#     def _sort_slices(self, slices: list) -> list:
#         slices.append('')  # for field 'note'
#         return slices


########################################
# English -> Russian
########################################


class English2RussianNoteTemplate(NoteTemplate):
    def __init__(self,
                 template_id=1002,
                 template_name='en2ru_Note',
                 fields: tuple = ('Word',
                                  'Audio',
                                  'Tags',
                                  'Translation',
                                  'Examples',
                                  'Notes',
                                  '_Version'),
                 front_format='formats/russian/english2russian/front.html',
                 back_format='formats/russian/english2russian/back.html',
                 css_format='formats/russian/english2russian/style.css'):
        super().__init__(template_id, template_name, fields,
                         front_format, back_format, css_format)


class English2RussianEncoder(Encoder):
    @staticmethod
    def _get_indexes(indexes_file: str, max_word_freq: int = None) -> list:
        with open(indexes_file, 'r') as file:
            indexes = [line.strip().split('\t')[0] for line in file
                       if int(line.strip().split('\t')[1]) <= max_word_freq]

        return indexes

    def _sort_slices(self, slices: list) -> list:
        word = slices[1]
        audio = f"[sound:{slices[1][:-1]}.mp3]"
        tags = tags_regex(slices[2])
        translation = translation_regex(slices[4])
        examples = examples_regex(slices[5])
        notes = ''
        _version = '1'
        return [word,
                audio,
                tags,
                translation,
                examples,
                notes,
                _version]


def tags_regex(string: str) -> str:
    return re.sub('\n', '<br>', string.strip('\n')).lower()


def translation_regex(string: str) -> str:
    translation_list = string.strip('\n').split('\n')

    _ = ['<ol>']
    for translation in translation_list:
        translation = re.sub('^', '<li>', translation)
        translation = re.sub('$', '</li>', translation)
        translation = re.sub('(Also|Example|Info)', ' <br> \\1', translation)
        translation = re.sub(' <br> (.*)$', ' <br> <span style="color: gray">\\1</span>', translation)
        _.append(translation)
    _.append('</ol>')

    return '\n'.join(_)


def examples_regex(string: str) -> str:
    example_list = string.strip('\n').split('\n')

    _ = ['<ul class=\"partial_list\">']
    for example in example_list:
        example = re.sub('^', '<li>', example)
        example = re.sub('$', '</li>', example)
        example = re.sub(' \| ', ' <br> ', example)
        example = re.sub(' <br> (.*)</li>', ' <br> <span style="color: gray">\\1</span></li>', example)
        _.append(example)
    _.append('</ul>')

    return '\n'.join(_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Let\'s build the Babel Tower!')
    parser.add_argument('-t', '--task', type=str, required=True,
                        choices=['chinese', 'english'],
                        help='')
    parser.add_argument('-i', '--index_file', type=str, required=True,
                        help='Path to the index file')
    parser.add_argument('-f', '--max_word_freq', type=int, required=True,
                        help='Path to the index file')
    parser.add_argument('-d', '--metadataset_path', type=str, required=True,
                        help='Path to the metadataset dir')
    parser.add_argument('-m', '--mediaset_path', type=str, required=True,
                        help='Path to the mediaset dir')
    parser.add_argument('-s', '--save_path', type=str, default='outputs',
                        help='Path to the save dir')
    parser.add_argument('-c', '--check_only', action='store_true',
                        help='')
    args = parser.parse_args()

    if not os.path.isdir(args.save_path):
        os.makedirs(args.save_path)

    if args.task == 'chinese':
        # logger = create_logger(logger_file=f'{args.save_path}/encode_ch2ru.log',
        #                        logger_name='encode_ch2ru')
        #
        # russian_template = Chinese2RussianNoteTemplate()
        # russian_encoder = Chinese2RussianEncoder(template=russian_template,
        #                                          divider='++++++++++',
        #                                          logger=logger)
        raise NotImplementedError
    elif args.task == 'english':
        logger = create_logger(logger_file=f'{args.save_path}/encode_en2ru.log',
                               logger_name='encode_en2ru')

        russian_template = English2RussianNoteTemplate()
        russian_encoder = English2RussianEncoder(template=russian_template,
                                                 divider='++++++++++',
                                                 logger=logger)
    else:
        raise NotImplementedError

    russian_encoder(
        deck_id=1001 if args.task == 'chinese' else 1002,
        deck_name='俄语卡组',
        save_path=args.save_path,
        indexes_file=args.index_file,
        metadataset_path=args.metadataset_path,
        mediaset_path=args.mediaset_path,
        check_only=args.check_only,
        max_word_freq=args.max_word_freq
    )
