import json

import spacy
import numpy

from agents.text_formaliser import TEXTS_REGULAR_EXPRESSIONS


def calculate_similarity(texts_file_path: str, similarity_file_path: str):
    nlp = spacy.load('en_core_web_lg')
    text_to_texts_similarities = dict()
    with open(file=texts_file_path) as texts_file:
        texts_map = json.load(fp=texts_file)
    
    for base_text, texts_string in texts_map.items():
        texts = set()
        text_matches = TEXTS_REGULAR_EXPRESSIONS.findall(string=texts_string)
        for text_match in text_matches:
            text = text_match[1].strip()
            texts.add(text)
        average_similarity = (
            __calculate_similarity_between_base_text_and_texts(
                nlp=nlp,
                base_text=base_text,
                texts=texts,
                text_to_texts_similarities=text_to_texts_similarities))
        print(base_text, average_similarity)
    
    with open(file=similarity_file_path, mode='w') as similarity_file:
        json.dump(obj=text_to_texts_similarities, fp=similarity_file, indent=4)


def __calculate_similarity_between_base_text_and_texts(text_to_texts_similarities: dict, base_text: str, texts: set, nlp) -> float:
    base_doc = nlp(base_text)
    average_similarity = 0.0
    for text in texts:
        text_doc = nlp(text)
        base_to_text_similarity = base_doc.similarity(text_doc)
        average_similarity += base_to_text_similarity
        text_to_texts_similarities[(base_text, text).__str__()] = base_to_text_similarity
    average_similarity = average_similarity / len(texts)
    return average_similarity
        

calculate_similarity(
    texts_file_path='../midputs/texts.json',
    similarity_file_path='../outputs/texts_similarities.json')
    
        
