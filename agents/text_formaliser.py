import json
import re

import backoff
import openai
from openai import RateLimitError, APIError, OpenAI
from requests import Timeout
from tqdm import tqdm

from common import MODEL, backoff_handler
from inputs.examples import SAMPLE_FORMALISATIONS

TEXTS_REGULAR_EXPRESSIONS = re.compile(pattern='(\d\.\s+)"([^"]+)"(.+)')


@backoff.on_exception(backoff.expo, RateLimitError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, APIError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, Timeout, on_backoff=backoff_handler, max_tries=8)
def __get_response(query: str) -> str:
    common_system_message = \
        'Your task is to formalize a philosophy puzzle in CLIF language following the pattern provided from an upper-level ontology. Do not answer to the puzzle, just translate it into CLIF. If you do not know how to translate it, just say so. Note that CLIF is a language of formal logic.'
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": common_system_message},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens = 2048
    )
    
    return response.choices[0].message.content


def formalise_texts(english_texts_file_path: str, formalisations_file_path: str):
    formalisations = dict()
    with open(file=english_texts_file_path) as samples_file:
        samples = json.load(fp=samples_file)
    for sample, sample_string in tqdm(samples.items()):
        text_matches = TEXTS_REGULAR_EXPRESSIONS.findall(string=sample_string)
        for text_match in tqdm(text_matches):
            text = text_match[1].strip()
            sample_clif = SAMPLE_FORMALISATIONS[sample.strip()]
            prompt = \
                'Translate the puzzle below to the CLIF language using the following pattern.\n###' + \
                '###Pattern Starts###\n' + \
                'English:' + \
                sample + \
                'CLIF:' + \
                sample_clif + \
                '\n###Pattern Ends###\n' + \
                '###Puzzle Starts###\n' + \
                'English:\n' + \
                text + \
                '\nCLIF:\n'
            response = __get_response(query=prompt)
            formalisations[text] = response
            
    with open(file=formalisations_file_path, mode='w') as formalisations_file:
        json.dump(obj=formalisations,fp=formalisations_file)
        
        