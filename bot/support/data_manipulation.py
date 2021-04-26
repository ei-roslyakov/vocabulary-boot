import codecs
from typing import Dict

from loguru import logger

from terminaltables import AsciiTable

from yaml import safe_load


def load_dictionary(file_name: str, encoding: str = "utf-8") -> Dict:
    with codecs.open(file_name, "r", encoding) as input_file:
        return safe_load(input_file)


def bot_print_data(translation_block: Dict) -> str:
    header = ["Word", "Translation(s)"]
    data = [header]

    for k, v in translation_block.items():
        if isinstance(v, list) or (isinstance(v, tuple)):
            v = "\n".join(v)

        item = k, v
        data.append(item)

    table = AsciiTable(data)
    table.inner_row_border = True
    return table.table


def get_words_by_block(dictionary_data: Dict, command: str):
    logger.info(f"Loading data from '{command}' block")

    translations_block = dictionary_data.get(command)
    nice_presentation = bot_print_data(translations_block)

    return nice_presentation


def get_block_count(dictionary_data: Dict, command: str):
    translations_block = dictionary_data.get(command)
    count = len(translations_block)

    return count


def get_words_by_block_one_by_one(dictionary_data: Dict, command: str, count: int):
    translations_block = dictionary_data.get(str(command))
    value_at_index = list(translations_block.keys())[count]

    return value_at_index


def get_words_by_block_with_answer(dictionary_data: Dict, command: str, word: str):
    translations_block = dictionary_data.get(str(command))
    value_at_index = translations_block[word]

    return value_at_index


def get_block_of_words(dictionary_data: Dict):
    numbers_of_block = {item for item in dictionary_data}

    return numbers_of_block


def get_all_blocks(dictionary_data: Dict):

    all_blocks = ""
    for block in dictionary_data:
        block = f"{str(block)}, "
        all_blocks = all_blocks + block

    return all_blocks
