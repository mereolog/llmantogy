import json
import os
import sys

from macleod.scripts.parser import parse_clif, clif_to_tptp
from macleod.src.p9_tools import parse
import macleod.parsing.parser as Parser

from puzzle_patterns import SAMPLE_FORMALISATIONS

TEMP_FILE_PATH = 'midputs/temp.clif'

with open(file='midputs/formalised_puzzles.json') as puzzle_json_file:
    json_puzzles = json.load(fp=puzzle_json_file)
verified_puzzles = dict()
verified_puzzles_tptp = dict()
faulty_puzzles = dict()
for puzzle_sample, puzzle in json_puzzles.items():
    with open(file=TEMP_FILE_PATH, mode='w') as temp_file:
        temp_file.write(puzzle)
    try:
        theory = Parser.parse_file(TEMP_FILE_PATH, sub='', base='')
        verified_puzzles[puzzle_sample] = puzzle
        verified_puzzles_tptp[puzzle_sample] = theory.to_tptp()
        # if puzzle_sample in verified_puzzles:
        #     verified_puzzles_for_sample = verified_puzzles[puzzle_sample]
        #     verified_puzzles_tptp_for_sample = verified_puzzles_tptp[puzzle_sample]
        # else:
        #     verified_puzzles_for_sample = list()
        #     verified_puzzles_tptp_for_sample = list()
        #     verified_puzzles[puzzle_sample] = verified_puzzles_for_sample
        #     verified_puzzles_tptp[puzzle_sample] = verified_puzzles_tptp_for_sample
        # verified_puzzles_for_sample.append(puzzle)
        # verified_puzzles_tptp_for_sample.append(theory.to_tptp())
    except TypeError as error:
        if puzzle_sample in faulty_puzzles:
            faulty_puzzles_for_sample = faulty_puzzles[puzzle_sample]
        else:
            faulty_puzzles_for_sample = list()
            faulty_puzzles[puzzle_sample] = faulty_puzzles_for_sample
        faulty_puzzles_for_sample.append(puzzle)
    os.remove(TEMP_FILE_PATH)
    
with open(file='midputs/faulty_formalised_puzzles.json', mode='w') as faulty_json_file:
    json.dump(obj=faulty_puzzles, fp=faulty_json_file, indent=4)
with open(file='midputs/verified_formalised_puzzles.json', mode='w') as verified_json_file:
    json.dump(obj=verified_puzzles, fp=verified_json_file, indent=4)
with open(file='midputs/verified_formalised_puzzles_tptp.json', mode='w') as verified_tptp_json_file:
    json.dump(obj=verified_puzzles_tptp, fp=verified_tptp_json_file, indent=4)