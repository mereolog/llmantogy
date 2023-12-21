from agents.clif_verifier import verify_formalised_texts
from agents.mil_verifier import semantically_verify_consistent_translations
from agents.puzzle_finder import find_similar_texts
from agents.puzzle_formaliser import formalise_texts
from agents.tptp_consistency_checker import check_texts_internal_consistency, check_texts_external_consistency

find_similar_texts(
    puzzles_file_path='midputs/texts.json')

formalise_texts(
    puzzles_file_path='midputs/texts.json',
    formalisations_file_path='midputs/formalised_texts.json')

verify_formalised_texts(
    formalised_puzzles_file_path='midputs/formalised_texts.json',
    faulty_formalised_puzzles_file_path='midputs/faulty_formalised_texts.json',
    verified_formalised_puzzles_file_path='midputs/verified_formalised_texts.json',
    tptp_puzzles_file_path='midputs/verified_formalised_texts_tptp.json')

check_texts_internal_consistency(
    tptp_puzzles_file_path='midputs/verified_formalised_texts_tptp.json',
    consistent_tptp_puzzles_file_path='outputs/internal_consistent_texts_tptp.json',
    inconsistent_tptp_puzzles_file_path='outputs/internally_inconsistent_texts_tptp.json',
    undecided_tptp_puzzles_file_path='outputs/internally_undecided_texts_tptp.json')

check_texts_external_consistency(
    tptp_puzzles_file_path='outputs/internal_consistent_texts_tptp.json',
    consistent_tptp_puzzles_file_path='outputs/dolce_consistent_texts_tptp.json',
    inconsistent_tptp_puzzles_file_path='outputs/dolce_inconsistent_texts_tptp.json',
    undecided_tptp_puzzles_file_path='outputs/dolce_undecided_texts_tptp.json',
    external_theory_file_path='inputs/dolce.tptp')

semantically_verify_consistent_translations(
    clif_syntactically_verified_texts_file_path='midputs/verified_formalised_texts.json',
    tptp_consistent_texts_file_path='outputs/dolce_consistent_texts_tptp.json',
    clif_semantically_accepted_texts_file_path='outputs/semantically_accepted_texts.json',
    clif_semantically_rejected_texts_file_path='outputs/semantically_rejected_texts.json')
