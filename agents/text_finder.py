import json

import backoff
from openai import RateLimitError, APIError, OpenAI
from requests import Timeout
from tqdm import tqdm

from common import MODEL, backoff_handler
from inputs.examples import SAMPLE_FORMALISATIONS


@backoff.on_exception(backoff.expo, RateLimitError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, APIError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, Timeout, on_backoff=backoff_handler, max_tries=8)
def __get_response(query: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": query},
        ],
        temperature=0.0,
    )
    
    return response.choices[0].message.content


def find_similar_texts(texts_file_path: str):
    texts = dict()
    for sample in tqdm(SAMPLE_FORMALISATIONS.keys()):
        prompt = \
            'In philosophical papers and books find 7 fragments that are most similar to the text below. Answer with the actual quotes from philosophy and not with their interpretations.\nText:' + \
            sample
        response = __get_response(query=prompt)
        texts[sample] = response
    with open(file=texts_file_path, mode='w') as texts_file:
        json.dump(obj=texts, indent=4, fp=texts_file)

