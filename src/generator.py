import logging
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

__all__ = ['Generator']


class Generator(ABC):
    r"""Abstract class for a generator that processes data based on indexes.
        Subclasses must implement the `_get_metadata` method.

    Args:
        save_path (str): The path to the directory where the generated files
            will be saved.
        divider (str): The character used to separate different parts of the
            generated output.
        functions: Functions used to generate the output based on the input
            data.
        logger (logging.Logger): A logger object used to print progress and
            other messages.
        overwrite (bool, optional): Whether to overwrite previously generated
            files. Defaults to False.
    """

    def __init__(self, save_path: str, divider: str,
                 functions, logger: logging.Logger,
                 overwrite: bool = False) -> None:
        # Create the output directory if it does not exist
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        self.metadata_path = os.path.join(save_path, 'metadata')
        if not os.path.exists(self.metadata_path):
            os.mkdir(self.metadata_path)
        self.media_path = os.path.join(save_path, 'media')
        if not os.path.exists(self.media_path):
            os.mkdir(self.media_path)

        self.divider = divider
        self.functions = functions
        self.logger = logger
        self.overwrite = overwrite

    def _get_indexes(self, indexes_file: str) -> list:
        r"""Reads the input indexes from a file.

        Args:
            indexes_file (str): The path to the file containing the input
                indexes.

        Returns:
            list: A list of input indexes to be processed.
        """
        with open(indexes_file, 'r') as file:
            indexes = [line.strip().split('\t')[0] for line in file
                       if self.overwrite or
                       not os.path.isfile(os.path.join(self.metadata_path,
                                                       line.strip().split('\\t')[0] + '.txt'))]
        self.logger.info(f'Reading `{len(indexes)}` words to be processed from '
                         f'`{indexes_file}`.')

        return indexes

    @abstractmethod
    def _get_metadata(self, index: str) -> None:
        r"""Abstract method to be implemented by subclasses.

        Args:
            index (str): The input index to be processed.
        """
        pass

    def __call__(self, indexes_file: str, num_threads: int = 4) -> None:
        r"""Calls the generator to process the input indexes.

        Args:
            indexes_file (str): The path to the file containing the input
                indexes.
            num_threads (int): The number of threads to use for processing.
                Default is 4.
        """
        indexes = self._get_indexes(indexes_file)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(self._get_metadata, index)
                       for index in indexes]
            with tqdm(total=len(indexes), unit='word') as pbar:
                for _ in as_completed(futures):
                    pbar.update(1)


if __name__ == '__main__':
    pass
