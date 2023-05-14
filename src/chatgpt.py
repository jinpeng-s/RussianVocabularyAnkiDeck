import logging
import os

import openai

__all__ = ['ChatGPT']


class ChatGPT:
    r"""A class for generating responses using the OpenAI API.

    Args:
        api_key (str): The OpenAI API key.
        engine (str): The name of the GPT-3 engine to use.
        prompt (str): The text prompt to use for generating responses.
        articulation (str): Additional text to add to the prompt for better
            articulation.
        logger (logging.Logger): A logger object for logging errors.
        max_retries (int, optional): The maximum number of retries to attempt
            when calling the OpenAI API.

    """

    def __init__(self, api_key: str, engine: str, prompt: str, articulation: str,
                 logger: logging.Logger, max_retries: int = 5) -> None:

        # load the OpenAI api key
        openai.api_key = self._load_content(api_key)

        self.engine = engine
        self.prompt = f'{self._load_content(prompt)}\n{self._load_content(articulation)}'

        self.logger = logger
        self.max_retries = max_retries

    @staticmethod
    def _load_content(string: str) -> str:
        r"""Loads the content from a file if the string is a valid file path,
            otherwise returns the string itself.

        Args:
            string (str): The string to load content from.

        Returns:
            str: The loaded content or the original string.
        """
        if len(string) < 128 and os.path.isfile(string):
            with open(string, 'r') as f:
                return f.read().strip()
        else:
            return string

    def __call__(self, index: str) -> str:
        r"""Generates a response using the OpenAI API.

        Args:
            index (str): The index of the response to generate.

        Returns:
            str: The generated response.
        """
        for i in range(self.max_retries):
            try:
                response = openai.Completion.create(
                    prompt=f'{self.prompt}: {index}.\n',
                    engine=self.engine, max_tokens=2048)
                return "\n".join([s for
                                  s in response["choices"][0]["text"].split("\n")
                                  if s.strip()])
            except Exception as e:
                self.logger.error(f"Error getting response for `{index}`"
                                  f"({i + 1}/{self.max_retries}): {e}")

        return None  # noqa


if __name__ == '__main__':
    from src.logger import create_logger

    c = ChatGPT(api_key=r'../keys/1',
                engine='text-davinci-003',
                prompt=r'../resources/prompts/english2russian.txt',
                articulation='现在是第一个单词',
                logger=create_logger('1.log'))
    a = c(r'абзац')
    print(a)
