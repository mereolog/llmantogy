import json
import random
import re
import backoff

import openai
import tiktoken
from openai.error import RateLimitError, ServiceUnavailableError, APIError, Timeout
from tqdm import tqdm

from common import MODEL, backoff_handler

ENCODING = 'cl100k_base'
MODEL_COST = 0.000015
MAX_MALLS_SAMPLES = 50

SAMPLE_TEXT = """
Out of six samples find the one that matches best to the text below. If there is no match, answer 'No match'; otherwise answer giving the identifier of the match, for example, Sample6. Be concise.
Samples:
Sample1: There is a four-legged table made of wood. Some time later, a leg of the table is replaced. Even later, the table is demolished so it ceases to exist although the wood is still there after the demolition.
Sample2: A man is walking to the station, but before he gets there, he turns around and goes home.
Sample3: Mr. Potter is the teacher of class 2C at Shapism School and resigns at the beginning of the spring break. After the spring break, Mrs. Bumblebee replaces Mr. Potter as the teacher of 2C. Also, student Mary left the class at the beginning of the break and a new student, John, joins in when the break ends.
Sample4: A flower is red in the summer. As time passes, the color changes. In autumn the flower is brown.
Sample5: A man is walking when suddenly he starts walking faster and then breaks into a run.
Sample6: Marriage is a contract between two people that is present in most social and cultural systems and it can change in major (e. g. gender constraints) and minor (e.g. marriage breaking procedures) aspects. Marriage is a contract that is regulated by civil and social constraints. These constraints can change but the meaning of marriage continues over time.
Text: """

SAMPLE_RE = re.compile(pattern='Sample\d')

def __count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding(ENCODING)
    num_tokens = len(encoding.encode(text))
    return num_tokens


@backoff.on_exception(backoff.expo, RateLimitError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, ServiceUnavailableError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, APIError, on_backoff=backoff_handler, max_tries=8)
@backoff.on_exception(backoff.expo, Timeout, on_backoff=backoff_handler, max_tries=8)
def __get_response(query: str) -> str:
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Your task is to find sentences semantically similar to a set of sample texts."},
            {"role": "user", "content": query},
        ],
        temperature=0.0
    )
    return response['choices'][0]['message']['content']
    
    
def select_matching_texts(texts_file: str, matching_texts_file: str, unmatching_texts_file: str):
    with open(file=texts_file) as malls_file:
        malls_data = json.load(malls_file)
    random.shuffle(malls_data)

    cost = 0
    nomatches = str()
    matches = dict()
    for malls_datum in tqdm(malls_data):
        nl_mall_text = malls_datum['NL']
        query = SAMPLE_TEXT + nl_mall_text
        query = query.strip()
        nl_text_token_length = __count_tokens(text=query)
        cost += nl_text_token_length*MODEL_COST
        best_match = __get_response(query=query)
        if 'No match'.lower() in best_match.lower():
            nomatches += nl_mall_text + '\n'
        else:
            matched_sample_id = SAMPLE_RE.findall(string=best_match)[0]
            matches[nl_mall_text] = matched_sample_id
        if len(matches) >= 50 or cost > 10:
            break
    
    with open(file=unmatching_texts_file, mode='w') as nomatches_file:
        nomatches_file.write(nomatches)
    with open(file=matching_texts_file, mode='w') as matches_file:
        json.dump(obj=matches,fp=matches_file)
        
select_matching_texts(texts_file='MALLS-v0.json', matching_texts_file='nonmatches.txt', unmatching_texts_file='matches.txt')





