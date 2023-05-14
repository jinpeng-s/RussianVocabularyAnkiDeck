import logging
import os
from abc import ABC, abstractmethod

import genanki
from tqdm import tqdm

__all__ = ['Encoder']


class Encoder(ABC):
    r"""An abstract class that provides encoding functionality to create Anki
        decks from given metadata and media files.

    Args:
        template (genanki.Model): An Anki note model containing fields to be
            filled with metadata.
        divider (str): A string used to separate different slices of metadata.
        logger (logging.Logger): A logger object to record encoding progress
            and errors.
    """

    def __init__(self, template: genanki.Model,
                 divider: str, logger: logging.Logger) -> None:

        self.template = template
        self.divider = divider
        self.logger = logger

    def _get_media_list(self, indexes_file: str, mediaset_path: str) -> list:
        r"""Reads a list of indexes from a file, and returns a list of
            corresponding media file paths.

        Args:
            indexes_file (str): A path to a file containing a list of indexes,
                each on a new line.
            mediaset_path (str): A path to a directory containing media files.

        Returns:
            A list of media file paths.
        """
        with open(indexes_file, 'r') as file:
            indexes = [line.strip().split('\t')[0] for line in file]
        self.logger.info(f'Reading {len(indexes)} words to be processed from '
                         f'`{indexes_file}`.')

        media_list = list()
        for index in indexes:
            index_path = os.path.join(mediaset_path, f'{index}.mp3')
            if os.path.isfile(index_path):
                media_list.append(index_path)
            else:
                self.logger.error(f'Media `{index}` is not in dataset `{mediaset_path}`, '
                                  f'skipping...')

        return media_list

    def _get_metadata_list(self, indexes_file: str, metadataset_path: str) -> list:
        r"""Reads a list of indexes from a file, and returns a list of
            corresponding metadata slices.

        Args:
            indexes_file (str): A path to a file containing a list of indexes,
                each on a new line.
            metadataset_path (str): A path to a directory containing metadata
                files.

        Returns:
            A list of lists, where each inner list contains metadata slices
                for a single index.
        """
        with open(indexes_file, 'r') as file:
            indexes = [line.strip().split('\t')[0] for line in file]
        self.logger.info(f'Reading {len(indexes)} words to be processed from '
                         f'`{indexes_file}`.')

        metadata_list = list()
        for index in indexes:
            index_path = os.path.join(metadataset_path, f'{index}.txt')
            if os.path.isfile(index_path):
                with open(index_path, "r") as file:
                    metadata_slices = file.read().strip().split(self.divider)
                    metadata_slices = list(filter(None, metadata_slices))
                    metadata_slices = self._sort_slices(metadata_slices)
                    # TODO 添加HTML regex
                    if len(metadata_slices) == len(self.template.fields):
                        metadata_list.append(metadata_slices)
                    else:
                        self.logger.error(f'Incorrect metadata format for `{index}`. '
                                          f'Expecting metadata to have '
                                          f'{len(self.template.fields)} fields, '
                                          f'but got {len(metadata_slices)} fields '
                                          f'instead, skipping...')
            else:
                self.logger.error(f'Word `{index}` is not in dataset `{metadataset_path}`, '
                                  f'skipping...')

        return metadata_list

    @abstractmethod
    def _sort_slices(self, slices: list) -> list:
        r"""Sorts the slices in the required order before encoding. This method
            must be implemented by all child classes.

        Args:
            slices: A list of slices to be sorted.

        Returns:
            A list of sorted slices.
        """
        pass

    def _encode_deck(self, deck: genanki.Deck,
                     metadata: list) -> None:
        r"""Encodes the given metadata into Anki notes and adds them to the
            given deck.

        Args:
            deck: The Anki deck to which the notes are to be added.
            metadata: A list of lists, where each inner list represents the
                metadata of a note.

        Returns:
            None.
        """
        pbar = tqdm(total=len(metadata), unit='word')
        for idx, slices in enumerate(metadata):
            deck.add_note(genanki.Note(
                model=self.template,
                fields=slices))
            pbar.update(1)
        pbar.close()
        self.logger.info(f'End of encoding deck `{deck.name}`.')

    def check(self, save_path: str, indexes_file: str,
              dataset_list: list, suffix_list: list) -> None:
        r"""Checks if the files corresponding to the given indexes exist in the
            specified dataset directories.

        Args:
            save_path: A string that represents the directory to save the
                .apkg file.
            indexes_file: The path to the file containing the list of indexes
                 to be checked.
            dataset_list: A list of paths to the directories containing the
                 dataset files.
            suffix_list: A list of suffixes to be appended to the indexes to
                 form the complete file names.

         Returns:
             None.
         """
        with open(indexes_file, 'r') as file:
            indexes = [line.strip().split('\t')[0] for line in file]
        self.logger.info(f'Reading {len(indexes)} words to be checked from '
                         f'`{indexes_file}`.')

        for dataset, suffix in zip(dataset_list, suffix_list):
            if not os.path.isdir(dataset):
                self.logger.error(f'Dataset `{dataset}` is not a directory, '
                                  f'skipping...')
            else:
                self.logger.info(f'Checking dataset `{dataset}`...')

            broken_list = list()
            for index in indexes:
                flag = os.path.isfile(os.path.join(dataset, f'{index}.{suffix}'))
                broken_list.append(index) if not flag else None
            self.logger.info(f'End of checking dataset `{dataset}`, '
                             f'[{len(broken_list)}/{len(indexes)}] broken '
                             f'indexes detected.')

            with open(os.path.join(save_path,
                                   f'{os.path.basename(dataset)}_broken.txt'),
                      'w') as file:
                for index in broken_list:
                    file.write(str(index) + '\n')

    def __call__(self, deck_id: int, deck_name: str,
                 save_path: str, indexes_file: str,
                 metadataset_path: str, mediaset_path: str = None,
                 check_only: bool = False) -> None:
        r"""Encodes a deck and saves it as an .apkg file.

        Args:
            deck_id: An integer that represents the ID of the deck.
            deck_name: A string that represents the name of the deck.
            save_path: A string that represents the directory to save the
                .apkg file.
            indexes_file: A string that represents the path to the file
                containing the indexes of the metadata and media.
            metadataset_path: A string that represents the path to the metadata
                file.
            mediaset_path: A string that represents the path to the media
                file(s). Defaults to None.
            check_only: A boolean that indicates if only the existence of the
                files should be checked. Defaults to False.
        """

        if check_only:
            self.check(save_path=save_path,
                       indexes_file=indexes_file,
                       dataset_list=[metadataset_path, mediaset_path],
                       suffix_list=['txt', 'mp3'])
        else:
            metadata = self._get_metadata_list(indexes_file, metadataset_path)
            media = self._get_media_list(indexes_file, mediaset_path)

            deck = genanki.Deck(deck_id=deck_id,
                                name=deck_name)
            self._encode_deck(deck, metadata)

            package = genanki.Package(deck_or_decks=deck,
                                      media_files=media)

            package.write_to_file(os.path.join(save_path,
                                               f'{deck_id}_{deck_name}.apkg'))


if __name__ == '__main__':
    pass
