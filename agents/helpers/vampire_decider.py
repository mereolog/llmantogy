import logging
import os
import subprocess
import sys

from agents.consistency_result import ProverResult

default_vampire_modes = ['casc_sat', 'casc', 'portfolio']


def decide_whether_theory_is_consistent(theory_file_name: str, keep_temp_files=False) -> ProverResult:
    vampire_modes = default_vampire_modes.copy()
    vampire_input_file_name = theory_file_name
    vampire_output_file_name = theory_file_name + '.out'
    cmd_to_run_vampire = 'resources/vampire --mode ' + vampire_modes[0] + '  ' + vampire_input_file_name + ' > ' + vampire_output_file_name
    vampire_process = subprocess.Popen(cmd_to_run_vampire, shell=True)
    vampire_process.wait()
    vampire_has_decided = vampire_process.returncode == 0
    vampire_process.kill()
    if vampire_has_decided:
        check_result_file = open(vampire_output_file_name)
        check_result = check_result_file.read()
        if not keep_temp_files:
            os.remove(vampire_input_file_name)
            os.remove(vampire_output_file_name)
        if 'SZS status Unsatisfiable' in check_result:
            return ProverResult.INCONSISTENT
        if 'SZS status Satisfiable' in check_result:
            return ProverResult.CONSISTENT
        logging.error(msg='Vampire hit a bump' + str(vampire_process))
        sys.exit(-1)
    else:
        vampire_modes.pop(0)
        if len(vampire_modes) > 0:
            logging.info(msg='Trying mode ' + vampire_modes[0])
            return \
                decide_whether_theory_is_consistent(
                    theory_file_name=theory_file_name,
                    keep_temp_files=keep_temp_files)
        return ProverResult.UNDECIDED
