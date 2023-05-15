import os


def single_file_op(file_path, divider: str = '\n++++++++++\n'):
    with open(file_path, "r") as file:
        metadata_slices = file.read().strip().split(divider)

        # types = metadata_slices[2]
        # tags = metadata_slices[3]

    with open(file_path, "w") as file:
        file.write(divider.join(metadata_slices))


def list_dir(dir_path: str):
    return [os.path.join(dir_path, item)
            for item in os.listdir(dir_path)]


if __name__ == '__main__':
    path = r'/Users/sjp/Documents/Code/RussianVocabularyAnkiDeck/resources/datasets/russian/english/metadata/а́втор.txt'

    single_file_op(path)
