import json

import backoff
import openai
from openai import RateLimitError, APIError
from requests import Timeout
from tqdm import tqdm

from common import MODEL, backoff_handler
from inputs.puzzle_patterns import SAMPLE_FORMALISATIONS


@backoff.on_exception(backoff.expo, RateLimitError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, APIError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, Timeout, on_backoff=backoff_handler, max_tries=8)
def __get_response(query: str) -> str:
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": query},
        ],
        temperature=0.0,
    )
    
    return response['choices'][0]['message']['content']


def find_puzzles(puzzles_file_path: str):
    puzzles = dict()
    for sample in tqdm(SAMPLE_FORMALISATIONS.keys()):
        prompt = \
            'In philosophical papers and books find 7 fragments that are most similar to the text below. Answer with the actual quotes from philosophy and not with their interpretations.\nText:' + \
            sample
        response = __get_response(query=prompt)
        puzzles[sample] = response
    with open(file=puzzles_file_path, mode='w') as puzzles_file:
        json.dump(obj=puzzles, indent=4, fp=puzzles_file)

