import os
import re


def update_metadata_in_index_file(folder_path, index_file_path):
    with open(index_file_path, 'r') as index_file:
        lines = index_file.readlines()

    updated_lines = []

    for line in lines:
        line = line.strip()
        file_name = line.split('.')[0] + '.txt'  # 文件名为索引行中的第一列加上 '.txt'

        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                metadata_slices = file.read().strip().split('++++++++++')
                metadata_slices = list(filter(None, metadata_slices))
                rank = metadata_slices[2]
                rank = rank.split('\n')
                rank = list(filter(None, rank))

                _ = list()
                for item in rank:
                    if re.findall(r'(top [\d,]+)', item):
                        _.append(int(re.findall(r'([\d,]+)', item)[0].replace(',', '')))
                if len(_) == 0:
                    _.append(99999)

            line = file_name[:-4] + '\t' + str(_[0])

        updated_lines.append(line)

    updated_content = '\n'.join(updated_lines)

    with open(index_file_path, 'w') as index_file:
        index_file.write(updated_content)


# 示例调用
folder_path = r'/Users/sjp/Babel-Tower-of-Anki/resources/datasets/russian/english/metadata'
index_file_path = r'/Users/sjp/Babel-Tower-of-Anki/resources/indexes/russian.txt'

update_metadata_in_index_file(folder_path, index_file_path)
