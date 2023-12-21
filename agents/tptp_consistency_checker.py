import json

from tqdm import tqdm

from agents.consistency_result import ProverResult
from agents.helpers.vampire_decider import decide_whether_theory_is_consistent

temp_file_path = 'midputs/temp.tptp'


def __check_puzzles_consistency(
        tptp_puzzles_file_path: str,
        external_theory: str,
        consistent_tptp_puzzles_file_path: str,
        inconsistent_tptp_puzzles_file_path: str,
        undecided_tptp_puzzles_file_path: str):
    consistent_puzzles = dict()
    inconsistent_puzzles = dict()
    undecided_puzzles = dict()
    
    with open(file=tptp_puzzles_file_path) as tptp_puzzles_file:
        tptp_puzzles = json.load(fp=tptp_puzzles_file)
    for puzzle, tptp_axioms in tqdm(tptp_puzzles.items()):
        with open(file=temp_file_path, mode='w') as temp_tptp_file:
            temp_tptp_file.write(tptp_axioms + '\n' + external_theory)
        theory_is_consistent = decide_whether_theory_is_consistent(theory_file_name=temp_file_path)
        if theory_is_consistent == ProverResult.CONSISTENT:
            consistent_puzzles[puzzle] = tptp_axioms
        if theory_is_consistent == ProverResult.INCONSISTENT:
            inconsistent_puzzles[puzzle] = tptp_axioms
        if theory_is_consistent == ProverResult.UNDECIDED:
            undecided_puzzles[puzzle] = tptp_axioms
        
    with open(file=consistent_tptp_puzzles_file_path, mode='w') as faulty_json_file:
        json.dump(obj=consistent_puzzles, fp=faulty_json_file, indent=4)
    with open(file=inconsistent_tptp_puzzles_file_path, mode='w') as verified_json_file:
        json.dump(obj=inconsistent_puzzles, fp=verified_json_file, indent=4)
    with open(file=undecided_tptp_puzzles_file_path, mode='w') as verified_tptp_json_file:
        json.dump(obj=undecided_puzzles, fp=verified_tptp_json_file, indent=4)


def check_texts_internal_consistency(
        tptp_puzzles_file_path: str,
        consistent_tptp_puzzles_file_path: str,
        inconsistent_tptp_puzzles_file_path: str,
        undecided_tptp_puzzles_file_path: str):
    __check_puzzles_consistency(
        tptp_puzzles_file_path=tptp_puzzles_file_path,
        consistent_tptp_puzzles_file_path=consistent_tptp_puzzles_file_path,
        inconsistent_tptp_puzzles_file_path=inconsistent_tptp_puzzles_file_path,
        undecided_tptp_puzzles_file_path=undecided_tptp_puzzles_file_path,
        external_theory=str())
    
        

def check_texts_external_consistency(
        tptp_puzzles_file_path: str,
        external_theory_file_path: str,
        consistent_tptp_puzzles_file_path: str,
        inconsistent_tptp_puzzles_file_path: str,
        undecided_tptp_puzzles_file_path: str):
    with open(file=external_theory_file_path) as external_theory_file:
        external_theory = external_theory_file.read()
    __check_puzzles_consistency(
        tptp_puzzles_file_path=tptp_puzzles_file_path,
        consistent_tptp_puzzles_file_path=consistent_tptp_puzzles_file_path,
        inconsistent_tptp_puzzles_file_path=inconsistent_tptp_puzzles_file_path,
        undecided_tptp_puzzles_file_path=undecided_tptp_puzzles_file_path,
        external_theory=external_theory)
    

