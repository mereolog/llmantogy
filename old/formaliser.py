import json

import backoff
import openai
from openai.error import RateLimitError, ServiceUnavailableError, APIError, Timeout
from tqdm import tqdm

from patterns import SAMPLE_1_PATTERN, SAMPLE_2_PATTERN, SAMPLE_3_PATTERN, SAMPLE_4_PATTERN, SAMPLE_5_PATTERN, \
    SAMPLE_6_PATTERN
from common import MODEL, backoff_handler

SAMPLES_PATTERNS_MAP = \
    {
        'Sample1' : SAMPLE_1_PATTERN,
        'Sample2' : SAMPLE_2_PATTERN,
        'Sample3' : SAMPLE_3_PATTERN,
        'Sample4' : SAMPLE_4_PATTERN,
        'Sample5' : SAMPLE_5_PATTERN,
        'Sample6' : SAMPLE_6_PATTERN
    }


@backoff.on_exception(backoff.expo, RateLimitError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, ServiceUnavailableError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, APIError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, Timeout, on_backoff=backoff_handler, max_tries=8)
def __get_response(query: str) -> str:
    common_system_message = \
        'Your task is to formalize a single English sentence into CLIF formulas following the provided pattern from an upper-level ontology.' \
         # +'###'.join(list(SAMPLES_PATTERNS_MAP.values()))
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": common_system_message},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        frequency_penalty=1.0
    )
    
    return response['choices'][0]['message']['content']

def formalise_texts(nl_texts_file_path: str, formalisations_file_path: str):
    formalisations = dict()
    with open(file=nl_texts_file_path) as samples_file:
        samples = json.load(fp=samples_file)
    for text, sample_id in tqdm(samples.items()):
        sample_pattern = SAMPLES_PATTERNS_MAP[sample_id]
        prompt = \
        'Translate the English sentence below to the CLIF language using the following pattern.\n###' + \
        sample_pattern + \
        '###' + \
        '\nEnglish:\n' + \
        text + \
        '\nCLIF:'
        response = __get_response(query=prompt)
        formalisations[text] = response
    with open(file=formalisations_file_path, mode='w') as formalisations_file:
        json.dump(obj=formalisations,fp=formalisations_file)
        
        
formalise_texts(nl_texts_file_path='matches.txt', formalisations_file_path='formalised_matches.json')
