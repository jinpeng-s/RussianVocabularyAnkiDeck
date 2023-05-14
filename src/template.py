import os

import genanki

__all__ = ['NoteTemplate']


class NoteTemplate(genanki.Model):
    def __init__(self, template_id: int,
                 template_name: str,
                 fields: tuple = ('Front', 'Back'),
                 front_format: str = '',
                 back_format: str = '',
                 css_format: str = '') -> None:
        assert os.path.isfile(front_format), \
            '`{}` is not a file!'.format(front_format)
        assert os.path.isfile(back_format), \
            '`{}` is not a file!'.format(back_format)
        assert os.path.isfile(css_format), \
            '`{}` is not a file!'.format(css_format)

        fields = [{'name': field} for field in fields]
        templates = [{'name': 'BabelTowerCard',
                      'qfmt': open(front_format, 'r', encoding='utf-8').read(),
                      'afmt': open(back_format, 'r', encoding='utf-8').read()}]
        css = open(css_format, 'r', encoding='utf-8').read()

        super().__init__(model_id=template_id, name=template_name,
                         fields=fields, templates=templates, css=css)


if __name__ == '__main__':
    my_model = NoteTemplate(
        template_id=6,
        template_name='BabelTowerNote',
        front_format='../formats/front.html',
        back_format='../formats/back.html',
        css_format='../formats/style.css'
    )

    my_note = genanki.Note(
        model=my_model,
        fields=['aaaaaa1111', 'BBBB'])

    my_deck = genanki.Deck(
        6,
        'Country Capitals')

    my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('output.apkg')
