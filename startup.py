from agents.clif_verifier import verify_formalised_puzzles
from agents.mil_verifier import semantically_verify_consistent_translations
from agents.puzzle_formaliser import formalise_puzzles
from agents.tptp_consistency_checker import check_puzzles_internal_consistency, check_puzzles_external_consistency

# find_puzzles(
#     puzzles_file_path='midputs/puzzles.json')
#
# formalise_puzzles(
#     puzzles_file_path='midputs/puzzles.json',
#     formalisations_file_path='midputs/formalised_puzzles.json')
#
# verify_formalised_puzzles(
#     formalised_puzzles_file_path='midputs/formalised_puzzles.json',
#     faulty_formalised_puzzles_file_path='midputs/faulty_formalised_puzzles.json',
#     verified_formalised_puzzles_file_path='midputs/verified_formalised_puzzles.json',
#     tptp_puzzles_file_path='midputs/verified_formalised_puzzles_tptp.json')

# check_puzzles_internal_consistency(
#     tptp_puzzles_file_path='midputs/verified_formalised_puzzles_tptp.json',
#     consistent_tptp_puzzles_file_path='outputs/internal_consistent_puzzles_tptp.json',
#     inconsistent_tptp_puzzles_file_path='outputs/internal_inconsistent_puzzles_tptp.json',
#     undecided_tptp_puzzles_file_path='outputs/internal_undecided_puzzles_tptp.json')

# check_puzzles_external_consistency(
#     tptp_puzzles_file_path='outputs/internal_consistent_puzzles_tptp.json',
#     consistent_tptp_puzzles_file_path='outputs/dolce_consistent_puzzles_tptp.json',
#     inconsistent_tptp_puzzles_file_path='outputs/dolce_inconsistent_puzzles_tptp.json',
#     undecided_tptp_puzzles_file_path='outputs/dolce_undecided_puzzles_tptp.json',
#     external_theory_file_path='inputs/dolce.tptp')

semantically_verify_consistent_translations(
    clif_syntactically_verified_texts_file_path='midputs/verified_formalised_puzzles.json',
    tptp_consistent_texts_file_path='outputs/dolce_consistent_puzzles_tptp.json')
