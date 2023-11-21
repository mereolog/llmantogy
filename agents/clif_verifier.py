import json

from macleod.logical.axiom import Axiom

from agents.helpers.macleod_parser import parse_clif

TEMP_FILE_PATH = 'midputs/temp.clif'

def verify_formalised_puzzles(
        formalised_puzzles_file_path: str,
        faulty_formalised_puzzles_file_path: str,
        verified_formalised_puzzles_file_path: str,
        tptp_puzzles_file_path: str):

    with open(file=formalised_puzzles_file_path) as puzzle_json_file:
        json_puzzles = json.load(fp=puzzle_json_file)
    verified_puzzles = dict()
    verified_puzzles_tptp = dict()
    faulty_puzzles = dict()
    for puzzle_sample, clif_puzzle in json_puzzles.items():
        try:
            clif_sentences = parse_clif(clif_text=clif_puzzle)
            verified_puzzles[puzzle_sample] = clif_puzzle
            tptp_theory = '\n'.join([clif_sentence.to_tptp() for clif_sentence in clif_sentences])
            verified_puzzles_tptp[puzzle_sample] = tptp_theory
        except TypeError as error:
            if puzzle_sample in faulty_puzzles:
                faulty_puzzles_for_sample = faulty_puzzles[puzzle_sample]
            else:
                faulty_puzzles_for_sample = list()
                faulty_puzzles[puzzle_sample] = faulty_puzzles_for_sample
            faulty_puzzles_for_sample.append(clif_puzzle)
        
    with open(file=faulty_formalised_puzzles_file_path, mode='w') as faulty_json_file:
        json.dump(obj=faulty_puzzles, fp=faulty_json_file, indent=4)
    with open(file=verified_formalised_puzzles_file_path, mode='w') as verified_json_file:
        json.dump(obj=verified_puzzles, fp=verified_json_file, indent=4)
    with open(file=tptp_puzzles_file_path, mode='w') as verified_tptp_json_file:
        json.dump(obj=verified_puzzles_tptp, fp=verified_tptp_json_file, indent=4)