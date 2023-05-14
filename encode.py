import argparse
import os

from src import create_logger, Encoder, NoteTemplate


########################################
# Chinese -> Russian
########################################


class Chinese2RussianNoteTemplate(NoteTemplate):
    def __init__(self,
                 template_id=1001,
                 template_name='BabelTowerNote',
                 fields: tuple = ('单词',
                                  '发音',
                                  '千亿释义',
                                  'AI释义',
                                  '笔记'),
                 front_format='formats/russian/chinese2russian/front.html',
                 back_format='formats/russian/chinese2russian/back.html',
                 css_format='formats/russian/chinese2russian/style.css'):
        super().__init__(template_id, template_name, fields,
                         front_format, back_format, css_format)


class Chinese2RussianEncoder(Encoder):
    def _sort_slices(self, slices: list) -> list:
        slices.append('')  # for field 'note'
        return slices


########################################
# English -> Russian
########################################


class English2RussianNoteTemplate(NoteTemplate):
    def __init__(self,
                 template_id=1002,
                 template_name='demoBabelTowerNote',
                 fields: tuple = ('单词',
                                  '发音',
                                  '千亿释义',
                                  '千亿释义',
                                  'AI释义',
                                  'AI释义',
                                  '笔记'),
                 front_format='formats/russian/english2russian/front.html',
                 back_format='formats/russian/english2russian/back.html',
                 css_format='formats/russian/english2russian/style.css'):
        super().__init__(template_id, template_name, fields,
                         front_format, back_format, css_format)


class English2RussianEncoder(Encoder):
    def _sort_slices(self, slices: list) -> list:
        slices.append('')  # for field 'note'
        return slices


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Let\'s build the Babel Tower!')
    parser.add_argument('-t', '--task', type=str, required=True,
                        choices=['chinese', 'english'],
                        help='')
    parser.add_argument('-i', '--index_file', type=str, required=True,
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
        logger = create_logger(logger_file=f'{args.save_path}/encode_ch2ru.log',
                               logger_name='encode_ch2ru')

        russian_template = Chinese2RussianNoteTemplate()
        russian_encoder = Chinese2RussianEncoder(template=russian_template,
                                                 divider='++++++++++',
                                                 logger=logger)
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
        check_only=args.check_only
    )

    # python encode.py -t chinese -i resources/indexes/test.txt -d outputs/ch2ru/metadata -m outputs/ch2ru/media -s outputs/ch2ru
