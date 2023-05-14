import argparse
import os

from src import create_logger, Crawler, ChatGPT, Generator


class Chinese2RussianGenerator(Generator):
    def _get_metadata(self, index: str) -> None:
        metadata_list = self.functions(index)
        metadata = '\n++++++++++\n'.join(metadata_list)

        with open(os.path.join(self.metadata_path, f'{metadata_list[1]}.txt'), 'w') as f:
            f.write(metadata)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Let\'s build the Babel Tower!')
    parser.add_argument('-t', '--task', type=str, required=True,
                        choices=['chinese', 'english'],
                        help='')
    parser.add_argument('-k', '--api_key', type=str, required=True,
                        help='Path to the index file')
    parser.add_argument('-i', '--index_file', type=str, required=True,
                        help='Path to the index file')
    parser.add_argument('-s', '--save_path', type=str, default='outputs',
                        help='Path to the save dir')
    parser.add_argument('-n', '--num_threads', type=int, default=4,
                        help='Number of threads to use for processing.')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Whether to overwrite previously generated files.')
    args = parser.parse_args()

    if not os.path.isdir(args.save_path):
        os.makedirs(args.save_path)

    if args.task == 'chinese':
        logger = create_logger(logger_file=f'{args.save_path}/gene_ch2ru.log',
                               logger_name='gene_ch2ru')
        crawler = Crawler(logger=logger)
        chatgpt = ChatGPT(api_key=args.api_key,
                          engine='text-davinci-003',
                          prompt=r'resources/prompts/english2russian.txt',
                          articulation='现在是第一个单词',
                          logger=logger)
    else:
        raise NotImplementedError

    generator = Chinese2RussianGenerator(save_path=args.save_path,
                                         divider='\n++++++++++\n',
                                         functions=crawler,
                                         logger=logger,
                                         overwrite=args.overwrite)

    generator(indexes_file=args.index_file,
              num_threads=args.num_threads)

    # python generate.py -t chinese -k keys/1 -s outputs -i resources/indexes/test.txt -n 5
