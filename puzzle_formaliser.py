import json
import re

import backoff
import openai
from openai.error import RateLimitError, ServiceUnavailableError, APIError, Timeout
from tqdm import tqdm

from old.patterns import SAMPLE_1_PATTERN, SAMPLE_2_PATTERN, SAMPLE_3_PATTERN, SAMPLE_4_PATTERN, SAMPLE_5_PATTERN, \
    SAMPLE_6_PATTERN
from common import MODEL, backoff_handler
from puzzle_patterns import SAMPLE_FORMALISATIONS

PUZZLES_REGULAR_EXPRESSIONS = re.compile(pattern='(\d\.\s+)"([^"]+)"(.+)')

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
        'Your task is to formalize a philosophy puzzle in CLIF language following the pattern provided from an upper-level ontology. Do not answer to the puzzle, just translate it into CLIF. If you do not know how to translate it, just say so. Note that CLIF is a language of formal logic.'
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": common_system_message},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens = 2048
    )
    
    return response['choices'][0]['message']['content']

def formalise_puzzles(puzzles_file_path: str, formalisations_file_path: str):
    formalisations = dict()
    with open(file=puzzles_file_path) as samples_file:
        samples = json.load(fp=samples_file)
    for sample, puzzles_string in tqdm(samples.items()):
        puzzle_matches = PUZZLES_REGULAR_EXPRESSIONS.findall(string=puzzles_string)
        for puzzle_match in tqdm(puzzle_matches):
            puzzle = puzzle_match[1].strip()
            puzzle_source = puzzle_match[2]
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
                puzzle + \
                '\nCLIF:\n'
            response = __get_response(query=prompt)
            formalisations[puzzle] = response
    with open(file=formalisations_file_path, mode='w') as formalisations_file:
        json.dump(obj=formalisations,fp=formalisations_file)
        
        
formalise_puzzles(puzzles_file_path='midputs/puzzles.json', formalisations_file_path='midputs/formalised_puzzles.json')
