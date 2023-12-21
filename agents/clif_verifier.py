import json

from agents.helpers.macleod_parser import parse_clif

TEMP_FILE_PATH = 'midputs/temp.clif'

def verify_formalised_texts(
        formalised_texts_file_path: str,
        faulty_formalised_texts_file_path: str,
        verified_formalised_texts_file_path: str,
        tptp_text_file_path: str):

    with open(file=formalised_texts_file_path) as text_json_file:
        json_texts = json.load(fp=text_json_file)
    verified_formalisations = dict()
    verified_formalisation_tptp = dict()
    faulty_formalisations = dict()
    for sample, clif_text in json_texts.items():
        try:
            clif_sentences = parse_clif(clif_text=clif_text)
            verified_formalisations[sample] = clif_text
            tptp_theory = '\n'.join([clif_sentence.to_tptp() for clif_sentence in clif_sentences])
            verified_formalisation_tptp[sample] = tptp_theory
        except TypeError as error:
            if sample in faulty_formalisations:
                faulty_formalisaitons_for_sample = faulty_formalisations[sample]
            else:
                faulty_formalisaitons_for_sample = list()
                faulty_formalisations[sample] = faulty_formalisaitons_for_sample
            faulty_formalisaitons_for_sample.append(clif_text)
        
    with open(file=faulty_formalised_texts_file_path, mode='w') as faulty_json_file:
        json.dump(obj=faulty_formalisations, fp=faulty_json_file, indent=4)
    with open(file=verified_formalised_texts_file_path, mode='w') as verified_json_file:
        json.dump(obj=verified_formalisations, fp=verified_json_file, indent=4)
    with open(file=tptp_text_file_path, mode='w') as verified_tptp_json_file:
        json.dump(obj=verified_formalisation_tptp, fp=verified_tptp_json_file, indent=4)